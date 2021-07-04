import unittest
import sys

from classopt import ClassOpt


@ClassOpt
class Opt:
    arg_int: int
    arg_str: str
    arg_float: float


class TestClassOpt(unittest.TestCase):
    def test_classopt(self):
        sys.argv.append("--arg_int")
        sys.argv.append("5")
        sys.argv.append("--arg_str")
        sys.argv.append("hello")
        sys.argv.append("--arg_float")
        sys.argv.append("3.2")

        opt = Opt.from_args()

        assert opt.arg_int == 5
        assert opt.arg_str == "hello"
        assert opt.arg_float == 3.2

        del sys.argv[1:]
