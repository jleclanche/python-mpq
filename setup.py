#!/usr/bin/env python
from setuptools import Extension, setup


module = Extension(
	"mpq.storm",
	sources=["mpq/stormmodule.cc"],
	language="c++",
	libraries=["storm"],
)

setup(ext_modules=[module])
