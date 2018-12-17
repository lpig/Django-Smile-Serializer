#!/usr/bin/env python

from setuptools import setup, find_packages

VERSION = '1.0.4'

url = "https://github.com/lpig/Django-Smile-Serializer"

long_description = "Django-Smile-Serializer"

setup(name="Django-Smile-Serializer",
      version=VERSION,
      description=long_description,
      maintainer="l-pig",
      maintainer_email="o55662000@yeah.net",
      url=url,
      long_description=long_description,
      install_requires=[
          'arrow',
          'six',
      ],
      packages=find_packages('.'),
      )
