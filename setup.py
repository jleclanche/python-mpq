#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
from distutils.core import setup, Extension

#README = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

CLASSIFIERS = [
	"Development Status :: 5 - Production/Stable",
	"Intended Audience :: Developers",
	"License :: OSI Approved :: MIT License",
	"Programming Language :: Python",
]

module = Extension("storm", sources=["storm/stormmodule.cc"], language="c++", libraries=["StormLib"], extra_compile_args=["-O0"])

setup(
	name = "python-storm",
	ext_modules = [module],
	author = "Jerome Leclanche",
	author_email = "adys.wh@gmail.com",
	classifiers = CLASSIFIERS,
	description = "Python bindings for StormLib",
	download_url = "http://github.com/Adys/python-storm/tarball/master",
	#long_description = README,
	url = "http://github.com/Adys/python-storm",
	version = "1.0",
)
