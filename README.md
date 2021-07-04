<h1 align="center">Welcome to ClassOpt 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000" />
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
from classopt import ClassOpt

@ClassOpt
class Opt:
    arg_int: int
    arg_str: str

if __name__ == "__main__":
    opt = Opt.from_args()
    print(opt.arg_int, opt.arg_str)
```

Run with command line arguments.

```bash
$ python main.py --arg_int 5 --arg_str hello
5 hello
```

## Advanced Usage

`ClassOpt` internally uses the standard libraries [dataclasses](https://docs.python.org/ja/3/library/dataclasses.html) and [argparse](https://docs.python.org/ja/3/library/argparse.html).
And you can specify the argument of `argparse.ArgumentParser.add_argument` with the `metadata` of `dataclasses.field`

```python
from dataclasses import field
from classopt import ClassOpt

@ClassOpt
class Opt:
    positional_arguments: str = field(
        metadata={"name_or_flags": "positional_arguments"}
    )
    short_arg: str = field(metadata={"name_or_flags": "-s"})
    default_int: int = field(metadata={"default": 3})
    store_true: bool = field(metadata={"action": "store_true"})
    nargs: list = field(metadata={"nargs": "+", "type": int})

if __name__ == "__main__":
    opt = Opt.from_args()
    print(opt)
```

```bash
$ python main.py positional_arguments -s short_arg --store_true --nargs 1 2 3
Opt(positional_arguments='positional_arguments', short_arg='short_arg', default_int=3, store_true=True, nargs=[1, 2, 3])
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
