"""Test configuration."""

import shutil
from pathlib import Path

import pytest
import wikiman as wm

TESTS_ROOT = Path("tests/wiki")


def restore_wiki():
    """Restore the wiki directory."""

    shutil.rmtree(wm.ROOT)
    shutil.copytree(TESTS_ROOT, wm.ROOT)


@pytest.fixture()
def wiki_directory():
    """Restore the wiki directory before any test that depends on it."""

    restore_wiki()


@pytest.fixture(scope="session", autouse=True)
def test_session():
    """Restore the wiki directory after finishing all tests."""

    yield
    restore_wiki()
