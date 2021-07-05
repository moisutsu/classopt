import unittest
import sys

from classopt import ClassOpt, config


@ClassOpt
class Opt:
    arg_int: int
    arg_str: str
    arg_float: float


@ClassOpt()
class AdvancedUsageOpt:
    long_arg: str = config(name_or_flags="--long_arg")
    s: str = config(name_or_flags="-s")
    default_int: int = config(name_or_flags="--default_int", default=3)
    store_true: bool = config(name_or_flags="--store_true", action="store_true")
    nargs: list = config(name_or_flags="--nargs", nargs="+", type=int)


@ClassOpt(default_long=True)
class DefaultLongOpt:
    arg1: int
    arg2: str


class TestClassOpt(unittest.TestCase):
    def test_classopt(self):
        set_args("5", "hello", "3.2")

        opt = Opt.from_args()

        assert opt.arg_int == 5
        assert opt.arg_str == "hello"
        assert opt.arg_float == 3.2

        del_args()

    def test_advanced_usage(self):
        set_args(
            "--long_arg",
            "long_arg",
            "-s",
            "short_arg",
            "--store_true",
            "--nargs",
            "1",
            "2",
            "3",
        )

        opt = AdvancedUsageOpt.from_args()

        assert opt.long_arg == "long_arg"
        assert opt.s == "short_arg"
        assert opt.default_int == 3
        assert opt.store_true
        assert opt.nargs == [1, 2, 3]

        del_args()

    def test_default_long(self):
        set_args("--arg1", "3", "--arg2", "hello")

        opt = DefaultLongOpt.from_args()

        assert opt.arg1 == 3
        assert opt.arg2 == "hello"

        del_args()


def set_args(*args):
    for arg in args:
        sys.argv.append(arg)


def del_args():
    del sys.argv[1:]
