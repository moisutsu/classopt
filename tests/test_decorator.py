import sys
import unittest
from typing import List

import pytest

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
            nargs: List[int] = config(long=True, nargs="+", type=int)

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
        @classopt(default_long=True)
        class Opt:
            list_a: List[int] = config(nargs="+")
            list_b: List[str] = config(nargs="*")

        set_args("--list_a", "3", "2", "1", "--list_b", "hello", "world")

        opt = Opt.from_args()

        assert opt.list_a == [3, 2, 1]
        assert opt.list_b == ["hello", "world"]

        del_args()

    @pytest.mark.skipif(
        sys.version_info < (3, 9),
        reason="These version does not support `list` type with subscription.",
    )
    def test_generic_alias_for_python3_9_or_later(self):
        @classopt(default_long=True)
        class Opt:
            list_a: list[int] = config(nargs="+")
            list_b: list[str] = config(nargs="*")

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
            def error(self, message):
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

    def test_simple_default_value_passing(self):
        @classopt(default_long=True)
        class Opt:
            arg0: int = 3
            arg1: list = ["hello", "world"]
            arg2: int
            arg3: int = config(default=5)
            arg4: list = config(default=[1, 2, 3])
            arg5: str

        set_args("--arg5", "hello")

        opt = Opt.from_args()

        assert opt.arg0 == 3
        assert opt.arg1 == ["hello", "world"]
        assert opt.arg2 == None
        assert opt.arg3 == 5
        assert opt.arg4 == [1, 2, 3]
        assert opt.arg5 == "hello"

        del_args()

    def test_convert_default_value_type_to_specified_type(self):
        from pathlib import Path

        @classopt(default_long=True)
        class Opt:
            arg0: Path = "test.py"

        set_args()

        opt = Opt.from_args()

        assert opt.arg0 == Path("test.py")

        del_args()

    def test_args_from_scipt(self):
        @classopt
        class Opt:
            arg_int: int
            arg_str: str
            arg_float: float

        set_args("5", "hello", "3.2")

        opt1 = Opt.from_args()

        del_args()

        opt2 = Opt.from_args(["5", "hello", "3.2"])

        assert opt1.arg_int == opt2.arg_int
        assert opt1.arg_str == opt2.arg_str
        assert opt1.arg_float == opt2.arg_float

    def test_to_dict(self):
        from pathlib import Path
        from typing import List

        @classopt
        class Opt:
            arg_int: int
            arg_float: float
            arg_path: Path
            arg_list: List[str]

        set_args("3", "3.2", "test.txt", "a", "b", "c")

        opt = Opt.from_args()

        opt_dict = opt.to_dict()
        correct_dict = {
            "arg_int": 3,
            "arg_float": 3.2,
            "arg_path": Path("test.txt"),
            "arg_list": ["a", "b", "c"],
        }

        assert all(
            opt_dict[key] == correct_dict[key]
            for key in set(list(opt_dict.keys()) + list(correct_dict.keys()))
        )

        del_args()

    def test_from_dict(self):
        from pathlib import Path
        from typing import List

        @classopt
        class Opt:
            arg_int: int
            arg_float: float
            arg_path: Path
            arg_list: List[str]

        args_dict = {
            "arg_int": 3,
            "arg_float": 3.2,
            "arg_path": Path("test.txt"),
            "arg_list": ["a", "b", "c"],
        }

        opt = Opt.from_dict(args_dict)

        assert opt.arg_int == args_dict["arg_int"]
        assert opt.arg_float == args_dict["arg_float"]
        assert opt.arg_list == args_dict["arg_list"]

        del_args()

    def test_to_json(self):
        import tempfile
        from pathlib import Path
        from typing import List

        @classopt
        class Opt:
            arg_int: int
            arg_float: float
            arg_list: List[str]

        set_args("3", "3.2", "a", "b", "c")

        opt = Opt.from_args()

        correct_json = (
            """{"arg_int": 3, "arg_float": 3.2, "arg_list": ["a", "b", "c"]}"""
        )

        opt_json = opt.to_json()

        assert opt_json == correct_json

        temp_path = Path(tempfile.mkdtemp()) / "test.json"
        opt.to_json(temp_path)

        assert temp_path.read_text() == correct_json

        del_args()

    def test_from_json(self):
        import tempfile
        from pathlib import Path
        from typing import List

        @classopt
        class Opt:
            arg_int: int
            arg_float: float
            arg_list: List[str]

        content_json = (
            """{"arg_int": 3, "arg_float": 3.2, "arg_list": ["a", "b", "c"]}"""
        )

        opt = Opt.from_json(content_json)

        assert opt.arg_int == 3
        assert opt.arg_float == 3.2
        assert opt.arg_list == ["a", "b", "c"]

        temp_path = Path(tempfile.mkdtemp()) / "test.json"
        temp_path.write_text(content_json)

        opt = Opt.from_json(temp_path)

        assert opt.arg_int == 3
        assert opt.arg_float == 3.2
        assert opt.arg_list == ["a", "b", "c"]

        del_args()


def set_args(*args):
    del_args()  # otherwise tests fail with e.g. "pytest -s"
    for arg in args:
        sys.argv.append(arg)


def del_args():
    del sys.argv[1:]
