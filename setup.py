#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()


setup_requirements = ["pytest-runner"]

test_requirements = ["pytest"]

setup(
    author="Ingo Rockel",
    author_email="ingo.rockel@gmail.com",
    description="Cloud Vision AI Sample",
    long_description=readme,
    include_package_data=True,
    name="ingredients_parser",
    packages=find_packages(include=["ingredients_parser"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    version="0.1.0",
    zip_safe=False,
)
