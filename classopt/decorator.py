import typing
from typing import TYPE_CHECKING, overload
from argparse import ArgumentParser
from dataclasses import dataclass

if TYPE_CHECKING:
    from typing import Literal, Callable, TypeVar, Type, Union, Generic
    _C = TypeVar("_C")
    _T = TypeVar("_T")
    
    class _ClassOptGeneric(Generic[_T]):
        @classmethod
        def from_args(cls) -> _T:
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

def classopt(cls=None, default_long=False, default_short=False):
    def wrap(cls):
        return _process_class(cls, default_long, default_short)

    if cls is None:
        return wrap

    return wrap(cls)


def _process_class(cls, default_long: bool, default_short: bool):
    @classmethod
    def from_args(cls):
        parser = ArgumentParser()

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

            generic_aliases = [typing._GenericAlias]
            try:
                from types import GenericAlias

                generic_aliases.append(GenericAlias)
            except ImportError:
                pass
            if (
                type(arg_field.type) in generic_aliases
                and arg_field.type.__origin__ == list
            ):
                kwargs["type"] = arg_field.type.__args__[0]
                if not "nargs" in arg_field.metadata:
                    kwargs["nargs"] = "*"

            if "type" in arg_field.metadata:
                kwargs["type"] = arg_field.metadata["type"]

            parser.add_argument(*name_or_flags, **kwargs)

        args = parser.parse_args()
        return cls(**vars(args))

    setattr(cls, "from_args", from_args)

    return dataclass(cls)
