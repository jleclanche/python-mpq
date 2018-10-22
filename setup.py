#!/usr/bin/env python
import platform
from setuptools import Extension, setup


extra_link_args = []
extra_compile_args = []
# XCode for macOS Mojave issue
if platform.mac_ver()[0] == "10.14":
	for flags in extra_link_args, extra_compile_args:
		flags += ["-stdlib=libc++", "-mmacosx-version-min=10.9"]


module = Extension(
	"mpq.storm",
	sources=["mpq/stormmodule.cc"],
	language="c++",
	libraries=["storm"],
	extra_compile_args=extra_compile_args,
	extra_link_args=extra_link_args,
)

setup(ext_modules=[module])
