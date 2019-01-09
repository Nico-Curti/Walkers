| **Authors**  | **Project** | **Build Status**              | **Latest Version** | **License** |
|:------------:|:-----------:|:-----------------------------:|:------------------:|:-----------:|
|   N. Curti   |   Walkers   | **Linux/MacOS** : [![Travis](https://travis-ci.com/Nico-Curti/Walkers.svg?branch=master)](https://travis-ci.com/Nico-Curti/Walkers) <br/> **Windows** : [![appveyor](https://ci.appveyor.com/api/projects/status/x7sbj6atp1a9cwuv?svg=true)](https://ci.appveyor.com/project/Nico-Curti/walkers)  | ![version](https://img.shields.io/badge/PyPI-v1.0.0-orange.svg?style=plastic) | ![license](https://img.shields.io/badge/license-GPL-blue.svg?style=plastic)

[![GitHub pull-requests](https://img.shields.io/github/issues-pr/Nico-Curti/walkers.svg?style=plastic)](https://github.com/Nico-Curti/walkers/pulls)
[![GitHub issues](https://img.shields.io/github/issues/Nico-Curti/walkers.svg?style=plastic)](https://github.com/Nico-Curti/walkers/issues)

[![GitHub stars](https://img.shields.io/github/stars/Nico-Curti/walkers.svg?label=Stars&style=social)](https://github.com/Nico-Curti/walkers/stargazers)
[![GitHub watchers](https://img.shields.io/github/watchers/Nico-Curti/walkers.svg?label=Watch&style=social)](https://github.com/Nico-Curti/walkers/watchers)

<a href="https://github.com/UniboDIFABiophysics">
<div class="image">
<img src="https://cdn.rawgit.com/physycom/templates/697b327d/logo_unibo.png" width="90" height="90">
</div>
</a>

# Random Walkers Simulator

The Walkers toolbox provides a set of optimization algorithms and random walk process inspired by natural process and physical equations. The package also includes a set of common score functions (landscape) to study the characteristics of each walkers and the pro and cons of each optimization strategy.

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Usage](#usage)
3. [Background](#background)
4. [Contribution](#contribution)
4. [Authors](#authors)
5. [Acknowledgement](#Acknowledgement)

## Prerequisites

**Walkers** support a pure Python implementation and a pure C++ version. To install the two components see the section below.

The **Python version** depends only by the most common scientific libraries (NumPy, SciPy, Matplotlib).

The **C++ version** supports only c++ standard 17 and needs OpenGL to perform walker visualization. To enable the multithreading support just build the files with the OMP flags ON.

## Installation

For the **Python installation** see [here](https://github.com/Nico-Curti/Walkers/tree/master/Walkers/docs/python_install.md).

For the **C++ installation** see [here](https://github.com/Nico-Curti/Walkers/tree/master/Walkers/docs/cpp_install.md).

For any troubles with the dependencies installation we recomend the use of [**ShUt**](https://github.com/Nico-Curti/shut) which includes a complete set of *no root* users installation scripts.

**NOTE:** In the Python version the directory [wip](https://github.com/Nico-Curti/Walkers/tree/master/Walkers/wip) includes incomplete and untested methods that are *work in progress* yet.

**NOTE:** The C++ version is incomplete and untested yet so pay attention to use it! I will finish it ASAP (compatibly with my social life).

## Usage

**Walkers** includes a large set of landscape functions commonly used in optimization algorithms testing. These functions are supported either in the Python version either in the C++ one and they are extracted from [https://www.sfu.ca/~ssurjano/optimization.html](https://www.sfu.ca/~ssurjano/optimization.html).

Each Python source code includes a small *__main__* function to test and show how to use it also in relation with the other codes. A complete example is given in [test.py](https://github.com/Nico-Curti/Walkers/blob/master/Walkers/tests/main.py).

Regard the C++ implementation a fully example is given in [run.cpp](https://github.com/Nico-Curti/Walkers/blob/master/example/run.cpp) which is also the only real cpp file in the project. All the optimization algorihtms are available just including the single header [walkers.h](https://github.com/Nico-Curti/Walkers/blob/master/cpp/include/walkers.h).

## Background

The Walkers project is inspired by the [EvoloPy](https://github.com/7ossam81/EvoloPy) project and it is proposed as an optimization and extension of that.

## Contribution

Any contribution is more than welcome :heart:. Just fill an issue or a pull request and I will check ASAP!

## Authors

* **Nico Curti** [git](https://github.com/Nico-Curti), [unibo](https://www.unibo.it/sitoweb/nico.curti2)

See also the list of [contributors](https://github.com/Nico-Curti/walkers/contributors) who partecipated in this project.

## Acknowledgments

Thanks goes to all contributors of this project:

[<img src="https://avatars1.githubusercontent.com/u/41203427?s=400&v=4" width="100px;"/><br /><sub><b>Dott.ssa Silvia Vitali</b></sub>](https://github.com/silviavitali)<br />

