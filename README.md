<h1 align="center">Welcome to ClassOpt 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1.4-blue.svg?cacheSeconds=2592000" />
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

Import `ClassOpt` and define the Opt class with decorator.

```python
from classopt import ClassOpt, config

@ClassOpt
class Opt:
    file: str
    count: int = config(long=True)
    numbers: list = config(long=True, short=True, nargs="+", type=int)
    debug: bool = config(long=True, short=True, action="store_true")

if __name__ == "__main__":
    opt = Opt.from_args()
    print(opt)
    print(opt.file)
```

Run with command line arguments.

```bash
$ python example.py example.txt --count 5 -n 1 2 3 --debug
Opt(file='example.txt', count=5, numbers=[1, 2, 3], debug=True)
example.txt
```
You can specify most of the arguments to [argparse.ArgumentParser.add_argument](https://docs.python.org/ja/3/library/argparse.html#argparse.ArgumentParser.add_argument) in `config` (except name_or_flags).

You can also use the long option by default.

```python
from classopt import ClassOpt, config

@ClassOpt(default_long=True)
class Opt:
    file: str = config(long=False)
    count: int
    numbers: list = config(nargs="+", type=int)
    debug: bool = config(action="store_true")

if __name__ == "__main__":
    opt = Opt.from_args()
    print(opt)
```

```bash
$ python example.py example.txt --count 5 --numbers 1 2 3 --debug
Opt(file='example.txt', count=5, numbers=[1, 2, 3], debug=True)
```

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
