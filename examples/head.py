from pathlib import Path
from classopt import ClassOpt, config


@ClassOpt
class Opt:
    input_file: Path
    lines: int = config(
        long=True, short="-n", default=10, help="print the first LINES lines"
    )
    index: bool = config(
        long=True, short=True, action="store_true", help="number all output lines"
    )


def main(opt: Opt):
    prefix_width = len(str(opt.lines))
    with opt.input_file.open() as f:
        for line_number, line in enumerate(f, 1):
            prefix = f"{str(line_number).rjust(prefix_width)}: " if opt.index else ""
            print(f"{prefix}{line}", end="")
            if line_number >= opt.lines:
                break


if __name__ == "__main__":
    opt = Opt.from_args()
    main(opt)
