# pylint: disable=missing-module-docstring, missing-function-docstring

from pathlib import Path
import shutil

import pytest

SRC = Path("./tests/wiki")
DST = Path("./wiki")


@pytest.fixture()
def restore_wiki():
    yield
    shutil.rmtree(DST)
    shutil.copytree(SRC, DST)
