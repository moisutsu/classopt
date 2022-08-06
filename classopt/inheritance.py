import typing
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")


class ClassOpt:
    @classmethod
    def _parser_factory(cls: T) -> ArgumentParser:
        return ArgumentParser()

    @classmethod
    def from_args(cls: T) -> T:
        parser = cls._parser_factory()

        for arg_name, arg_type in cls.__annotations__.items():
            kwargs = {}

            metadata = {}
            if hasattr(cls, arg_name):
                metadata.update(getattr(cls, arg_name).metadata)

            kwargs.update(metadata)
            kwargs["type"] = arg_type
            kwargs.pop("long", None)
            kwargs.pop("short", None)

            name_or_flags = []
            if isinstance(metadata.get("long"), bool):
                if metadata.get("long"):
                    name_or_flags.append(f"--{arg_name}")

            if isinstance(metadata.get("short"), str):
                name_or_flags.append(metadata.get("short"))
            elif isinstance(metadata.get("short"), bool):
                if metadata.get("short"):
                    name_or_flags.append(f"-{arg_name[0]}")

            if len(name_or_flags) == 0:
                name_or_flags.append(arg_name)

            if "action" in metadata:
                kwargs.pop("type")
            elif arg_type == bool:
                kwargs.pop("type")
                kwargs["action"] = "store_true"

            generic_aliases = [typing._GenericAlias]
            try:
                from types import GenericAlias

                generic_aliases.append(GenericAlias)
            except ImportError:
                pass
            if type(arg_type) in generic_aliases and arg_type.__origin__ == list:
                kwargs["type"] = arg_type.__args__[0]
                if not "nargs" in metadata:
                    kwargs["nargs"] = "*"

            if "type" in metadata:
                kwargs["type"] = metadata["type"]

            parser.add_argument(*name_or_flags, **kwargs)

        args = parser.parse_args()

        return dataclass(cls)(**vars(args))
