import unittest
import sys

from classopt import ClassOpt, option


@ClassOpt
class Opt:
    arg_int: int
    arg_str: str
    arg_float: float


@ClassOpt()
class AdvancedUsageOpt:
    positional_arguments: str = option(name_or_flags="positional_arguments")
    short_arg: str = option(name_or_flags="-s")
    default_int: int = option(default=3)
    store_true: bool = option(action="store_true")
    nargs: list = option(nargs="+", type=int)


class TestClassOpt(unittest.TestCase):
    def test_classopt(self):
        set_args("--arg_int", "5", "--arg_str", "hello", "--arg_float", "3.2")

        opt = Opt.from_args()

        assert opt.arg_int == 5
        assert opt.arg_str == "hello"
        assert opt.arg_float == 3.2

        del_args()

    def test_advanced_usage(self):
        set_args(
            "positional_arguments",
            "-s",
            "short_arg",
            "--store_true",
            "--nargs",
            "1",
            "2",
            "3",
        )

        opt = AdvancedUsageOpt.from_args()

        assert opt.positional_arguments == "positional_arguments"
        assert opt.short_arg == "short_arg"
        assert opt.default_int == 3
        assert opt.store_true
        assert opt.nargs == [1, 2, 3]

        del_args()


def set_args(*args):
    for arg in args:
        sys.argv.append(arg)


def del_args():
    del sys.argv[1:]
