<h1 align="center">Welcome to ClassOpt 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/pypi/v/classopt" />
  <a href="https://github.com/moisutsu/classopt/blob/main/LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://twitter.com/moisutsu" target="_blank">
    <img alt="Twitter: moisutsu" src="https://img.shields.io/twitter/follow/moisutsu.svg?style=social" />
  </a>
</p>

> Arguments parser with class for Python, inspired by [StructOpt](https://github.com/TeXitoi/structopt)

## Install

```sh
pip install classopt
```

## Usage


Import `classopt` and define the Opt class with decorator.

```python
from classopt import classopt

@classopt(default_long=True)
class Opt:
    file: str
    count: int = 3
    numbers: list[int]
    flag: bool

if __name__ == "__main__":
    opt = Opt.from_args()
    print(opt)
    print(opt.file)
```

Run with command line arguments.

```bash
$ python example.py --file example.txt --numbers 1 2 3 --flag
Opt(file='example.txt', count=3, numbers=[1, 2, 3], flag=True)
example.txt
```
You can specify most of the arguments to [argparse.ArgumentParser.add_argument](https://docs.python.org/ja/3/library/argparse.html#argparse.ArgumentParser.add_argument) in `config` (except name_or_flags).


```python
from classopt import classopt, config

@classopt
class Opt:
    file: str
    count: int = config(long=True)
    numbers: list = config(long=True, short=True, nargs="+", type=int)
    flag: bool = config(long=True, action="store_false")

if __name__ == "__main__":
    opt = Opt.from_args()
    print(opt)
```

```bash
$ python example.py example.txt --count 5 -n 1 2 3 --flag
Opt(file='example.txt', count=5, numbers=[1, 2, 3], flag=False)
```

Some details
```python
# `default_long=True` is equivalent to `config(long=True)' for all members
# Similarly, you can do `default_short=True`
@classopt(default_long=True)
class Opt:
    # `long=False` overrides `default_long=True`
    file: str = config(long=False)

    # equivalent to `numbers: list = config(nargs="*", type=int)`
    # and `numbers: typing.List[int]`
    numbers: list[int]

    # equivalent to `flag: bool = config(action="store_true")`
    flag: bool
```

### Other Way

You can also define an argument parser by inheriting from `ClassOpt`.

```python
from classopt import ClassOpt, config

class Opt(ClassOpt):
    file: str
    count: int = config(long=True)
    numbers: list[int] = config(long=True, short="-c")
    flag: bool = config(long=True)

if __name__ == "__main__":
    opt = Opt.from_args()
    print(opt)
    print(opt.file)
```

Run with command line arguments.

```bash
$ python example.py example.txt --count 5 -c 1 2 3 --flag
Opt(file='example.txt', count=5, numbers=[1, 2, 3], flag=True)
example.txt
```

The inherited method does not support some features and may disappear in the future.
So we recommend the decorator method.

## Run tests

```sh
poetry run pytest
```

## Author

👤 **moisutsu**

* Twitter: [@moisutsu](https://twitter.com/moisutsu)
* Github: [@moisutsu](https://github.com/moisutsu)

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2021 [moisutsu](https://github.com/moisutsu).<br />
This project is [MIT](https://github.com/moisutsu/classopt/blob/main/LICENSE) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
