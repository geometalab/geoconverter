#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import versioneer
from setuptools import setup
from pip.req import parse_requirements

PACKAGE = 'src'
LONG = """This is an online data converter for GIS vector file formats.
It is based on the open source GDAL/OGR tools.
"""


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, _, _ in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_requirements():
    requirements_file_path = os.path.join(
        os.path.dirname(__file__),
        'requirements.txt')
    if os.path.exists(requirements_file_path):
        parsed_requirements = parse_requirements(
            requirements_file_path,
            session=False)
        requirements = [str(ir.req) for ir in parsed_requirements]
    else:
        requirements = []
    return requirements


setup(
    name="GeoConverter",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Josua Stähli",
    maintainer="Marcel Huber",
    maintainer_email="marcel.huber@hsr.ch",
    description="GIS file format converter",
    long_description=LONG,
    license="MIT",
    keywords=['GIS', 'format', 'converter', 'GDAL', 'OGR'],
    url="https://github.com/geometalab/geoconverter",
    packages=get_packages(PACKAGE),
    install_requires=get_requirements(),
    setup_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django :: 1.5",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Information Analysis"],
)
