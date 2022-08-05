import unittest
import sys

from classopt import ClassOpt, config


class TestClassOpt(unittest.TestCase):
    def test_classopt(self):
        class Opt(ClassOpt):
            arg_int: int
            arg_str: str
            arg_float: float

        set_args("5", "hello", "3.2")

        opt = Opt.from_args()

        assert opt.arg_int == 5
        assert opt.arg_str == "hello"
        assert opt.arg_float == 3.2

        del_args()

    def test_advanced_usage(self):
        class Opt(ClassOpt):
            long_arg: str = config(long=True)
            short_arg1: str = config(long=True, short=True)
            short_arg2: str = config(long=True, short="-x")
            default_int: int = config(long=True, default=3)
            store_true: bool = config(long=True, action="store_true")
            nargs: list = config(long=True, nargs="+", type=int)

        set_args(
            "--long_arg",
            "long_arg",
            "-s",
            "short_arg1",
            "-x",
            "short_arg2",
            "--store_true",
            "--nargs",
            "1",
            "2",
            "3",
        )

        opt = Opt.from_args()

        assert opt.long_arg == "long_arg"
        assert opt.short_arg1 == "short_arg1"
        assert opt.short_arg2 == "short_arg2"
        assert opt.default_int == 3
        assert opt.store_true
        assert opt.nargs == [1, 2, 3]

        del_args()

    def test_generic_alias(self):
        from typing import List

        class Opt(ClassOpt):
            list_a: List[int] = config(long=True, nargs="+")
            list_b: List[str] = config(long=True, nargs="*")

        set_args("--list_a", "3", "2", "1", "--list_b", "hello", "world")

        opt = Opt.from_args()

        assert opt.list_a == [3, 2, 1]
        assert opt.list_b == ["hello", "world"]

        del_args()

    def test_default_value(self):
        from typing import List
        class Opt(ClassOpt):
            numbers: List[int] = config(long=True)
            flag: bool = config(long=True)

        set_args("--numbers", "1", "2", "3", "--flag")

        opt = Opt.from_args()

        assert opt.numbers == [1, 2, 3]
        assert opt.flag

        del_args()

    def test_interactive_prompt(self):
        class Opt(ClassOpt):
            arg_int: int
            arg_str: str
            arg_float: float

        set_args("5", "hello", "3.2")

        opt1 = Opt.from_args()

        del_args()

        opt2 = Opt.from_args("5","hello","3.2")

        assert opt1.arg_int == opt2.arg_int
        assert opt1.arg_str == opt2.arg_str
        assert opt1.arg_float == opt2.arg_float


def set_args(*args):
    for arg in args:
        sys.argv.append(arg)


def del_args():
    del sys.argv[1:]
