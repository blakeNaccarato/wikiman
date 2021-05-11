"""CLI manager for GitHub Wikis."""

from pathlib import Path

from setuptools import find_packages, setup

long_description = (Path() / "README.md").read_text(encoding="utf-8")

setup(
    name="wikiman",
    version="0.3.0",
    description=("CLI manager for GitHub Wikis."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blakeNaccarato/wikiman",
    author="Blake Naccarato",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=["fire~=0.4", "markdown~=3.3", "GitPython~=3.1"],
    entry_points={
        "console_scripts": ["wikiman=wikiman.cli:main"],
    },
)
