"""Setup file for ImageQ package.
   @author
     Domnan Diretnan
     Artificial Intelligence Enthusiast & Python Developer
     Email: diretnandomnan@gmail.com 
     GitHub: https://github.com/deven96
   @project
     File: setup.py
   @license
     MIT License
     Copyright (c) 2018. Domnan Diretnan. All rights reserved.
"""

import os
import sys
import setuptools
from setuptools.command.install import install

CURRENT_DIR = os.getcwd()
REQUIREMENTS = 'requirements.txt'
requires = [line.strip('\n') for line in open(REQUIREMENTS).readlines()]
with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = "1.0.1"


setuptools.setup(
    name="ImageQ",
    version=VERSION,
    author='Domnan Diretnan, Mmadu Manasseh',
    author_email="diretnandomnan@gmail.com, mmadumanasseh@gmail.com",
    description="Image search engine powered by keras",
    url="https://github.com/bisoncorps/imageQ",
    packages=setuptools.find_packages(),
    install_requires=requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords='keras image search',
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    package_data={
        '': ['*.*'],
    },
    include_package_data=True,
)
