#!/usr/bin/env python
from distutils.core import setup, Extension


CLASSIFIERS = [
	"Development Status :: 5 - Production/Stable",
	"Intended Audience :: Developers",
	"License :: OSI Approved :: MIT License",
	"Programming Language :: Python",
	"Programming Language :: Python :: 3",
	"Programming Language :: Python :: 3.3",
	"Programming Language :: Python :: 3.4",
]

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
	download_url="http://github.com/hearthsim/python-mpq/tarball/master",
	url="https://github.com/hearthsim/python-mpq",
	version="1.0",
)
