#!/usr/bin/env python3

import os.path as osp

from setuptools import find_packages, setup


def readme():
    with open("README.md") as f:
        content = f.read()
    return content


def find_version():
    version_file = "dhole/version.py"  # avoid import issues while looking at __init__.py
    with open(version_file, "r") as f:
        exec(compile(f.read(), version_file, "exec"))
    return locals()["__version__"]


def get_requirements(filename="requirements.txt"):
    here = osp.dirname(osp.realpath(__file__))
    with open(osp.join(here, filename), "r") as f:
        requires = [line.replace("\n", "") for line in f.readlines()]
    return requires


def get_long_description():
    with open("README.md") as f:
        long_description = f.read()
    return long_description


setup(
    name="dhole",
    version=find_version(),
    install_requires=get_requirements(),
    include_package_data=True,
    packages=find_packages(),
    description="local docker server for research",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Haruya Ishikawa",
    author_email="haru.ishi43@gmail.com",
    license="MIT",
    url="https://github.com/haruishi43/local_docker_server",
    keywords=["Docker"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.6",
    zip_safe=False,
)
