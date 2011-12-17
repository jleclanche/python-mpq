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

DEBUG = False
compile_args = []
if DEBUG:
	compile_args.append("-O0")

module = Extension("mpq.storm", sources=["mpq/stormmodule.cc"], language="c++", libraries=["StormLib"], extra_compile_args=compile_args)

setup(
	name = "python-mpq",
	ext_modules = [module],
	packages = ["mpq"],
	author = "Jerome Leclanche",
	author_email = "adys.wh@gmail.com",
	classifiers = CLASSIFIERS,
	description = "Python bindings for StormLib",
	download_url = "http://github.com/Adys/python-mpq/tarball/master",
	#long_description = README,
	url = "http://github.com/Adys/python-mpq",
	version = "1.0",
)
