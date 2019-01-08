#!/usr/bin/python

# References: https://github.com/kennethreitz/setup.py

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta-data.
NAME = 'Walkers'
DESCRIPTION = 'Random Walkers and Nature-based Optimizer simulator.'
URL = 'https://github.com/Nico-Curti/Walkers'
EMAIL = 'nico.curti2@unibo.it'
AUTHOR = 'Nico Curti'
REQUIRES_PYTHON = '>=2.7'
VERSION = None
KEYWORDS = "random-walk optimization-algorithms nature-inspired-algorithms evolutionary-algorithms"

# What packages are required for this module to be executed?
def get_requires():
  with open('requirements.txt', 'r') as f:
    requirements = f.read()
  return list(filter(lambda x: x != '', requirements.split()))

# What packages are optional?
EXTRAS = {
  'tests': ['matplotlib'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
  with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()
except FileNotFoundError:
  long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
  with open(os.path.join(here, 'Walkers', '__version__.py')) as f:
    exec(f.read(), about)
else:
  about['__version__'] = VERSION

# Where the magic happens:
setup(
  name=NAME,
  version=about['__version__'],
  description=DESCRIPTION,
  long_description=long_description,
  long_description_content_type='text/markdown',
  author=AUTHOR,
  author_email=EMAIL,
  maintainer=AUTHOR,
  maintainer_email=EMAIL,
  python_requires=REQUIRES_PYTHON,
  url=URL,
  download_url=URL,
  keywords=KEYWORDS,
  packages=find_packages(include=['Walkers', 'Walkers.*'], exclude=('wip', 'test',)),
  # If your package is a single module, use this instead of 'packages':
  #py_modules=['walkers'],
  #
  # entry_points={
  #     'console_scripts': ['mycli=mymodule:cli'],
  # },
  install_requires=get_requires(),
  extras_require=EXTRAS,
  include_package_data=True,
  license='GNU Lesser General Public License v2 or later (LGPLv2+)',
  platforms='any',
  classifiers=[
    # Trove classifiers
    # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    'License :: OSI Approved :: GPL License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy'
  ],
)
