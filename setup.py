#!/usr/bin/env python
import platform
from setuptools import Extension, setup

if platform.system() != 'Darwin':
    extra_compile_args = ['-O3'] 
    extra_link_args = []
else:
    extra_compile_args = ['-O3', '-mmacosx-version-min=10.9', '-stdlib=libc++', '-Wdeprecated']
    extra_link_args = ['-stdlib=libc++', '-mmacosx-version-min=10.9']


module = Extension(
	"mpq.storm",
	sources=["mpq/stormmodule.cc"],
	language="c++",
	libraries=["storm"],
	include_dirs=["stormlib/src/"],
	library_dirs=["stormlib/"],
	extra_compile_args=extra_compile_args,
	extra_link_args=extra_link_args,
)

setup(ext_modules=[module])
