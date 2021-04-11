# pylint: disable=missing-function-docstring, missing-module-docstring, redefined-outer-name, unused-argument, wrong-import-order

from filecmp import dircmp

import pytest
import wikiman as wm
from pytest import mark as m

import conftest

# ! -------------------------------------------------------------------------------- ! #
# ! CLI

# ! -------------------------------------------------------------------------------- ! #
# ! BACKEND

# * -------------------------------------------------------------------------------- * #
# * FILE OPERATIONS

# * --------- * #
# * init_page

INIT_PAGE_RAISES_PARAMS = [
    # (
    #     <test_id>
    #     <args>
    # ),
    (
        "backslash",
        (
            "Backs\lash",  # noqa:W605, pylint:disable=anomalous-backslash-in-string
            wm.ROOT_PAGE,
            0,
        ),
    ),
    (
        "escape_sequences",
        ("E\as\bc\fa\np\re\ts\v", wm.ROOT_PAGE, 0),
    ),
    (
        "all_others",
        ('/:*?"<>|', wm.ROOT_PAGE, 0),
    ),
]


@m.parametrize("test_id, args", INIT_PAGE_RAISES_PARAMS)
def test_init_page_raises(test_id, args):

    with pytest.raises(ValueError):
        wm.init_page(*args)


INIT_PAGE_PARAMS = [
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


@m.parametrize("test_id, args, expected", INIT_PAGE_PARAMS)
def test_init_page(test_id, args, expected):

    result = wm.init_page(*args)

    assert result == expected


# * ----------- * #
# * create_page

# reuse params from init_page, but compare to `expected_wiki` instead of `expected`
CREATE_PAGE_PARAMS = [param[:2] for param in INIT_PAGE_PARAMS]


@m.parametrize("test_id, args", CREATE_PAGE_PARAMS)
def test_create_page(test_id, args, EXPECTED_WIKI):

    # TODO: Implement EXPECTED_WIKI for parametrized tests

    page = wm.init_page(*args)

    wm.create_page(page)
    result = dircmp(wm.WIKI_ROOT, EXPECTED_WIKI)

    assert not result.diff_files


# * --------- * #
# * find_page

FIND_PAGE_PARAMS = [
    # (
    #     <test_id>
    #     <arg>
    #     <expected>
    # ),
    (
        "root_page",
        wm.ROOT_PAGE.stem,
        wm.ROOT_PAGE,
    ),
    (
        "lowercase",
        "impeach-vermilion-vacuum",
        FIND_PAGE_LOWERCASE_EXPECTED := (
            conftest.WIKI_ROOT
            / r"00_Impeach-Vermilion-Vacuum\Impeach-Vermilion-Vacuum.md"
        ),
    ),
    (
        "uppercase",
        "Impeach-Vermilion-Vacuum",
        FIND_PAGE_LOWERCASE_EXPECTED,
    ),
]


@m.parametrize("test_id, arg, expected", FIND_PAGE_PARAMS)
def test_find_page(test_id, arg, expected, RESTORE_WIKI_BEFORE_TEST):

    result = wm.find_page(arg)

    assert result == expected


# * -------------------------------------------------------------------------------- * #
# * NAVIGATION

# * -------------------------------------------------------------------------------- * #
# * RELATIVES


@m.parametrize(
    "test_id, arg, expected",
    [
        (
            "root_page",
            wm.ROOT_PAGE,
            wm.WIKI_ROOT / "Home.md",
        ),
    ],
)
def test_get_parent(test_id, arg, expected):

    result = wm.get_parent(arg)

    assert result == expected


# ! -------------------------------------------------------------------------------- ! #
# ! UTILITIES

# * -------------------------------------------------------------------------------- * #
# * MARKDOWN

# * -------------------------------------------------------------------------------- * #
# * STRINGS


@m.parametrize(
    "test_id, args, expected",
    [
        ("one_digit", ("page-name", 3), "03_page-name"),
        ("two_digits", ("page-name", 45), "45_page-name"),
    ],
)
def test_get_dir_name(test_id, args, expected):

    result = wm.get_dir_name(*args)

    assert result == expected


@m.parametrize(
    "test_id, arg, expected",
    [
        ("dashes", "page-with-dashes", "page-with-dashes"),
        ("spaces", "page with spaces", "page-with-spaces"),
    ],
)
def test_get_dashed_name(test_id, arg, expected):

    result = wm.get_dashed_name(arg)

    assert result == expected
