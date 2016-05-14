#!/usr/bin/env python
import os
from distutils.core import setup, Extension


CLASSIFIERS = [
	"Development Status :: 5 - Production/Stable",
	"Intended Audience :: Developers",
	"License :: OSI Approved :: MIT License",
	"Programming Language :: Python",
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.3",
	"Programming Language :: Python :: 3.4",
	"Programming Language :: Python :: 3.5",
]

README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

DEBUG = False
compile_args = []
if DEBUG:
	compile_args.append("-O0")

module = Extension("mpq.storm",
	sources=["mpq/stormmodule.cc"],
	language="c++",
	libraries=["storm"],
	extra_compile_args=compile_args
)

setup(
	name="mpq",
	ext_modules=[module],
	packages=["mpq"],
	author="Jerome Leclanche",
	author_email="jerome@leclan.ch",
	classifiers=CLASSIFIERS,
	description="Python bindings for StormLib",
	download_url="http://github.com/HearthSim/python-mpq/tarball/master",
	long_description=README,
	url="https://github.com/HearthSim/python-mpq",
	version="1.1.1",
)
