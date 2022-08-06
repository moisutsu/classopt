from pathlib import Path

from classopt import classopt, config


@classopt(default_long=True, default_short=True)
class Opt:
    a: int = 0
    b: int = config(default=1)
    c: Path = Path("./tmp.txt")
    d: list = config(default=[0, 1, 2], nargs="+", type=int)


if __name__ == "__main__":
    opt: Opt = Opt.from_args()
    print(opt)
