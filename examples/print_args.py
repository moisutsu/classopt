from classopt import classopt, config
from pathlib import Path

@classopt(default_long=True, default_short=True)
class Opt:
    x: int
    a: int = config(default=5)
    b: int = 10
    c: Path = "./tmp.txt"
    d: list = config(default=[0, 1, 2], nargs="+", type=int)


if __name__ == "__main__":
    opt = Opt.from_args()
    print(opt)