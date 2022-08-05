import unittest
import sys

from classopt import classopt, config


class TestClassOpt(unittest.TestCase):
    def test_classopt(self):
        @classopt
        class Opt:
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
        @classopt()
        class Opt:
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

    def test_default_long(self):
        @classopt(default_long=True)
        class Opt:
            arg0: str = config(long=False)
            arg1: int
            arg2: str

        set_args("hogehoge", "--arg1", "3", "--arg2", "hello")

        opt = Opt.from_args()

        assert opt.arg0 == "hogehoge"
        assert opt.arg1 == 3
        assert opt.arg2 == "hello"

        del_args()

    def test_default_short(self):
        @classopt(default_long=True, default_short=True)
        class Opt:
            a_arg: int
            b_arg: str

        set_args("-a", "3", "-b", "hello")

        opt = Opt.from_args()

        assert opt.a_arg == 3
        assert opt.b_arg == "hello"

        del_args()

    def test_generic_alias(self):
        from typing import List

        @classopt(default_long=True)
        class Opt:
            list_a: List[int] = config(nargs="+")
            list_b: List[str] = config(nargs="*")

        set_args("--list_a", "3", "2", "1", "--list_b", "hello", "world")

        opt = Opt.from_args()

        assert opt.list_a == [3, 2, 1]
        assert opt.list_b == ["hello", "world"]

        del_args()

    def test_default_value(self):
        from typing import List
        @classopt(default_long=True)
        class Opt:
            numbers: List[int]
            flag: bool

        set_args("--numbers", "1", "2", "3", "--flag")

        opt = Opt.from_args()

        assert opt.numbers == [1, 2, 3]
        assert opt.flag

        del_args()

    def test_external_parser(self):
        from argparse import ArgumentParser
        class userArgumentParserException(Exception):
            pass

        class userArgumentParser(ArgumentParser):
            def error(self,message):
                raise userArgumentParserException()

        @classopt(parser=userArgumentParser())
        class Opt:
            arg_int: int
            arg_str: str
            arg_float: float

        set_args("5", "hello", "3.2")

        opt = Opt.from_args()

        assert opt.arg_int == 5
        assert opt.arg_str == "hello"
        assert opt.arg_float == 3.2

        del_args()

        set_args("5", "hello")

        with self.assertRaises(userArgumentParserException):
            opt = Opt.from_args()

        del_args()



def set_args(*args):
    del_args()  # otherwise tests fail with e.g. "pytest -s"
    for arg in args:
        sys.argv.append(arg)


def del_args():
    del sys.argv[1:]
