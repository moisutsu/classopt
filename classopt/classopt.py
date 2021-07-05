from argparse import ArgumentParser
from dataclasses import dataclass


def ClassOpt(cls=None, *settings):
    def wrap(cls):
        return _process_class(cls)

    if cls is None:
        return wrap

    return wrap(cls)


def _process_class(cls):
    @classmethod
    def from_args(cls):
        parser = ArgumentParser()

        for arg_name, arg_field in cls.__dataclass_fields__.items():
            kwargs = {}
            kwargs.update(arg_field.metadata)
            kwargs["type"] = arg_field.type

            name_or_flags = []
            if "name_or_flags" in arg_field.metadata:
                name_or_flags.append(arg_field.metadata["name_or_flags"])
                if arg_field.metadata["name_or_flags"].startswith("-"):
                    name_or_flags.append(f"--{arg_name}")
                kwargs.pop("name_or_flags")
            else:
                name_or_flags.append(f"--{arg_name}")

            if "action" in arg_field.metadata:
                kwargs.pop("type")

            if "type" in arg_field.metadata:
                kwargs["type"] = arg_field.metadata["type"]

            parser.add_argument(*name_or_flags, **kwargs)

        args = parser.parse_args()
        return cls(**vars(args))

    setattr(cls, "from_args", from_args)

    return dataclass(cls)
