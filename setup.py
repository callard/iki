#!/usr/bin/env python
import sys, os
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name="IKI",
      version="0.1dev",
      description="IKI's rebirth",
      packages = find_packages(),	  	  
      long_description="""\This is the brand new IKI""",
      author="A wild bunch of coder",
      author_email="ikiV2@googlegroups.com",
      url="http://iki-project.org/",
      )
