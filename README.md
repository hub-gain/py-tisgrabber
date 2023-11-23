# py-tisgrabber ‒ Wrapper for IC-Imaging-Control by the Imaging source for modern Python.



<!---
[![Conda](https://img.shields.io/conda/v/conda-forge/py_tisgrabber?color=blue&label=conda-forge)](https://anaconda.org/conda-forge/py_tisgrabber)
[![Build Status](https://travis-ci.com/bleykauf/py_tisgrabber.svg?branch=main)](https://travis-ci.com/bleykauf/py_tisgrabber)
[![Documentation Status](https://readthedocs.org/projects/py_tisgrabber/badge/?version=latest)](https://py_tisgrabber.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/bleykauf/py_tisgrabber/badge.svg?branch=main)](https://coveralls.io/github/bleykauf/py_tisgrabber?branch=main)
-->
[![PyPI](https://img.shields.io/pypi/v/py_tisgrabber?color=blue)](https://pypi.org/project/py_tisgrabber/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`py-tisgrabber` is a Python wrapper for the `tisgrabber.dll` and `tisgrabber_x64.dll` of the
IC Imaging Control SDK, allowing the control of cameras by [The Imaging Source](https://www.theimagingsource.com).
It works on Microsoft Windows and Python ≥ 3.11

This is similar to [`py-ic-imaging-control`](https://github.com/morefigs/py-ic-imaging-control) but
aims to be more pythonic (complies with PEP8 via black code style, proper use of Enums, @properties, some type hinting)
and easier to read. Also, the [official examples](https://github.com/TheImagingSource/IC-Imaging-Control-Samples/tree/master/Python)
have been recreated by using this wrapper.

## Installation

```
pip install py-tisgrabber
```

For running the [examples](./examples/), install the additional dependencies with

```
pip install py-tisgrabber[examples]
```

## Authors

-   Bastian Leykauf (<https://github.com/bleykauf>)

## License

MIT License

Copyright (c) 2022-2023 Bastian Leykauf

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.