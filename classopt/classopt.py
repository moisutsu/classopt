from argparse import ArgumentParser
from dataclasses import dataclass


def ClassOpt(cls):
    @classmethod
    def from_args(cls):
        parser = ArgumentParser()

        for arg_name, arg_field in cls.__dataclass_fields__.items():
            parser.add_argument(
                f"--{arg_name}", type=arg_field.type, **arg_field.metadata
            )

        args = parser.parse_args()
        return cls(**vars(args))

    setattr(cls, "from_args", from_args)

    return dataclass(cls)
