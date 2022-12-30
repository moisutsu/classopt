import typing
from argparse import ArgumentParser
from dataclasses import MISSING, Field, asdict, dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, overload

from classopt import config
from classopt.utils import (
    GENERIC_ALIASES,
    convert_non_primitives_to_string,
    revert_non_primitives_from_string,
)

if TYPE_CHECKING:
    from typing import Callable, Generic, Literal, Type, TypeVar, Union

    _C = TypeVar("_C")
    _T = TypeVar("_T")

    class _ClassOptGeneric(Generic[_T]):
        @classmethod
        def from_args(cls) -> _T:
            ...

        def to_dict(self) -> dict:
            ...

        @classmethod
        def from_dict(cls, data: dict) -> _T:
            ...


@overload
def classopt(
    cls: "Type[_C]",
    default_long: bool = False,
    default_short: bool = False,
) -> "Union[Type[_C], Type[_ClassOptGeneric[_C]]]":
    ...


@overload
def classopt(
    cls: "Literal[None]" = None,
    default_long: bool = False,
    default_short: bool = False,
) -> "Callable[[Type[_C]], Union[Type[_C], Type[_ClassOptGeneric[_C]]]]":
    ...


def classopt(cls=None, default_long=False, default_short=False, parser=None):
    def wrap(cls):
        return _process_class(cls, default_long, default_short, parser)

    if cls is None:
        return wrap

    return wrap(cls)


def _process_class(
    cls, default_long: bool, default_short: bool, external_parser: ArgumentParser
):
    @classmethod
    def from_args(cls, args: Optional[List[str]] = None):
        parser = external_parser if external_parser is not None else ArgumentParser()

        for arg_name, arg_field in cls.__dataclass_fields__.items():
            kwargs = {}
            kwargs.update(arg_field.metadata)
            kwargs["type"] = arg_field.type
            kwargs.pop("long", None)
            kwargs.pop("short", None)

            name_or_flags = []
            if isinstance(arg_field.metadata.get("long"), bool):
                if arg_field.metadata.get("long"):
                    name_or_flags.append(f"--{arg_name}")
            elif default_long:
                name_or_flags.append(f"--{arg_name}")

            if isinstance(arg_field.metadata.get("short"), str):
                name_or_flags.append(arg_field.metadata.get("short"))
            elif isinstance(arg_field.metadata.get("short"), bool):
                if arg_field.metadata.get("short"):
                    name_or_flags.append(f"-{arg_name[0]}")
            elif default_short:
                name_or_flags.append(f"-{arg_name[0]}")

            if len(name_or_flags) == 0:
                name_or_flags.append(arg_name)

            if "action" in arg_field.metadata:
                kwargs.pop("type")
            elif arg_field.type == bool:
                kwargs.pop("type")
                kwargs["action"] = "store_true"

            if (
                arg_field.default == MISSING and arg_field.default_factory == MISSING
            ) or arg_field.default is None:
                kwargs["default"] = None
            elif arg_field.default != MISSING:
                kwargs["default"] = arg_field.type(arg_field.default)
            elif arg_field.default_factory != MISSING:
                kwargs["default"] = arg_field.type(arg_field.default_factory())

            if (
                type(arg_field.type) in GENERIC_ALIASES
                and arg_field.type.__origin__ == list
            ):
                kwargs["type"] = arg_field.type.__args__[0]
                if not "nargs" in arg_field.metadata:
                    kwargs["nargs"] = "*"

            if "type" in arg_field.metadata:
                kwargs["type"] = arg_field.metadata["type"]

            parser.add_argument(*name_or_flags, **kwargs)

        ns = parser.parse_args(args=args)
        return cls(**vars(ns))

    for arg_name in cls.__annotations__.keys():
        if not hasattr(cls, arg_name):
            setattr(cls, arg_name, None)
        elif not isinstance(getattr(cls, arg_name), Field):
            setattr(cls, arg_name, config(default=getattr(cls, arg_name)))

    setattr(cls, "from_args", from_args)

    def to_dict(self):
        def classopt_dict_factory(items: List[Tuple[str, Any]]) -> Dict[str, Any]:
            converted_dict = {
                key: convert_non_primitives_to_string(value) for key, value in items
            }

            return converted_dict

        return asdict(self, dict_factory=classopt_dict_factory)

    setattr(cls, "to_dict", to_dict)

    @classmethod
    def from_dict(cls, data: dict):
        reverted_data = {
            key: revert_non_primitives_from_string(
                value, original_type=cls.__annotations__[key]
            )
            for key, value in data.items()
            if key in cls.__annotations__
        }

        return cls(**reverted_data)

    setattr(cls, "from_dict", from_dict)

    return dataclass(cls)
