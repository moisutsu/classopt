from argparse import ArgumentParser
from dataclasses import dataclass


def ClassOpt(cls=None, default_long: bool = False, default_short: bool = False):
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

            name_or_flags = []
            if default_long:
                name_or_flags.append(f"--{arg_name}")
            if default_short:
                name_or_flags.append(f"-{arg_name[0]}")

            if "name_or_flags" in arg_field.metadata:
                name_or_flags.append(arg_field.metadata["name_or_flags"])
                kwargs.pop("name_or_flags")

            if len(name_or_flags) == 0:
                name_or_flags.append(arg_name)

            if "action" in arg_field.metadata:
                kwargs.pop("type")

            if "type" in arg_field.metadata:
                kwargs["type"] = arg_field.metadata["type"]

            parser.add_argument(*name_or_flags, **kwargs)

        args = parser.parse_args()
        return cls(**vars(args))

    setattr(cls, "from_args", from_args)

    return dataclass(cls)
