# pylint: disable=missing-function-docstring, missing-module-docstring, redefined-outer-name, unused-argument, wrong-import-order

from filecmp import dircmp

import pytest
import wikiman as wm
from pytest import mark as m

# * -------------------------------------------------------------------------------- * #
# * FILE OPERATIONS


TEST_INIT_PAGE_PARAMS = [
    # (
    #     <test_id>
    #     <args>
    #     <expected>
    # ),
    (
        "dashes",
        ("test-page-name", wm.ROOT_PAGE, 0),
        wm.WIKI_ROOT / "00_test-page-name/test-page-name.md",
    ),
    (
        "spaces",
        ("test page name", wm.ROOT_PAGE, 0),
        wm.WIKI_ROOT / "00_test-page-name/test-page-name.md",
    ),
]


@m.parametrize(
    "test_id, args",
    [param[:2] for param in TEST_INIT_PAGE_PARAMS],
)
def test_create_page(test_id, args, expected_wiki):

    (name, under, position) = args
    page = wm.init_page(name, under, position)
    wm.create_page(page)

    result = dircmp(wm.WIKI_ROOT, expected_wiki)

    assert not result.diff_files


@m.parametrize("name", tuple(wm.ILLEGAL_CHARACTERS.replace("\\", "")))
def test_init_page_raises(name):
    """Ensure that the proper exception is raised when illegal characters are given.

    We can't test for backslash because Python always escapes backslashes outside of an
    explicit raw string constant. Also, raw strings cannot end with a backslash, so a
    raw string containing a single backslash doesn't work either. So we test every other
    illegal character.

    https://docs.python.org/3/faq/design.html#why-can-t-raw-strings-r-strings-end-with-a-backslash
    """

    with pytest.raises(ValueError, match=wm.ILLEGAL_CHARACTERS) as excinfo:
        wm.init_page(name, wm.ROOT_PAGE, 0)

    assert wm.ILLEGAL_CHARACTERS in str(excinfo.value)


@m.parametrize("test_id, args, expected", TEST_INIT_PAGE_PARAMS)
def test_init_page(test_id, args, expected):

    (name, under, position) = args

    result = wm.init_page(name, under, position)

    assert result == expected


# * -------------------------------------------------------------------------------- * #
# * FAMILY


@m.parametrize(
    "test_id, args, expected",
    [
        (
            "root_page",
            wm.ROOT_PAGE,
            wm.WIKI_ROOT / "Home.md",
        ),
    ],
)
def test_get_parent(test_id, args, expected):

    (page) = args

    result = wm.get_parent(page)

    assert result == expected
