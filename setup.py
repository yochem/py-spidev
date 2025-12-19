#!/usr/bin/env python

from setuptools import setup

version = "0.0"

lines = [x for x in open("spidev_module.c").read().split("\n") if "#define" in x and "_VERSION_" in x and "\"" in x]

if len(lines) > 0:
    version = lines[0].split("\"")[1]
else:
    raise Exception("Unable to find _VERSION_ in spidev_module.c")

setup(
    version = version,
)