"""GitHub Wiki CLI manager."""

import pathlib

from setuptools import find_packages, setup

here = pathlib.Path().resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="wikiman",
    version="0.1.0",
    description=("GitHub Wiki CLI manager."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blakeNaccarato/wikiman",
    author="Blake Naccarato",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["markdown"],
)
