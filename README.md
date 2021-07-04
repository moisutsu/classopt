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
