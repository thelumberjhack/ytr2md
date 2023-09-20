#!/usr/bin/env python
# coding=utf-8
"""setuptools install script"""

import site

from setuptools import setup

site.ENABLE_USER_SITE = True


if __name__ == "__main__":
    setup()
