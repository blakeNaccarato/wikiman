# pylint: disable=missing-module-docstring, missing-function-docstring, unused-argument

from pathlib import Path

import pytest
import wikiman as wm

TESTS_ROOT = Path("tests/wiki")


@pytest.mark.parametrize("page, expected", [(wm.ROOT_PAGE, wm.ROOT / "Home.md")])
def test_get_parent(wiki_directory, page, expected):

    result = wm.get_parent(page)

    assert result == expected
