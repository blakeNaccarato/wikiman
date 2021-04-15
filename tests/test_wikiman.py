# pylint: disable=missing-function-docstring, missing-module-docstring, redefined-outer-name, unused-argument, wrong-import-order

from filecmp import dircmp

import pytest
import wikiman as wm
from pytest import mark as m

from conftest import WIKI_ROOT

# ! -------------------------------------------------------------------------------- ! #
# ! UTILITIES

# * -------------------------------------------------------------------------------- * #
# * STRINGS


# * ---------------------------------------- * #
# * get_dashed_name


@m.parametrize(
    "test_id, args, expected",
    [
        ("dashes", ("page-with-dashes",), "page-with-dashes"),
        ("spaces", ("page with spaces",), "page-with-spaces"),
    ],
)
def test_get_dashed_name(test_id, args, expected):
    result = wm.get_dashed_name(*args)
    assert result == expected


# * ---------------------------------------- * #
# * get_human_name


@m.parametrize(
    "test_id, args, expected",
    [
        ("dashes", ("page-with-dashes",), "page with dashes"),
        ("spaces", ("page with spaces",), "page with spaces"),
    ],
)
def test_get_human_name(test_id, args, expected):
    result = wm.get_human_name(*args)
    assert result == expected


# * ---------------------------------------- * #
# * get_md_name


@m.parametrize(
    "test_id, args, expected", [("base", ("Name of a page",), "Name-of-a-page.md")]
)
def test_get_md_name(test_id, args, expected):
    result = wm.get_md_name(*args)
    assert result == expected


# * ---------------------------------------- * #
# * get_dir_name


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


# * -------------------------------------------------------------------------------- * #
# * MARKDOWN


# * ---------------------------------------- * #
# * get_page_url


# We use `wm.GIT_REMOTE_URL` because we don't care about that part. That will resolve
# the wiki repo properly when invoked by end-users. Sure, it doesn't give us a "proper"
# wiki link in the test suite, since we're not invoking this from a "proper" wiki repo.
# And we can't pytest.fixtures.monkeypatch a module-level variable, either.
@m.parametrize(
    "test_id, args, expected", [("base", (wm.ROOT_PAGE,), wm.GIT_REMOTE_URL + "Home")]
)
def test_get_page_url(test_id, args, expected):
    result = wm.get_page_url(*args)
    assert result == expected


# * ---------------------------------------- * #
# * get_md_link


@m.parametrize("test_id, args, expected", [("base", ("text", "link"), "[text](link)")])
def test_get_md_link(test_id, args, expected):
    result = wm.get_md_link(*args)
    assert result == expected


# * ---------------------------------------- * #
# * get_page_link


@m.parametrize(
    "test_id, args, expected",
    [("base", (wm.ROOT_PAGE,), f"[Home]({wm.GIT_REMOTE_URL}Home)")],
)
def test_get_page_link(test_id, args, expected):
    result = wm.get_page_link(*args)
    assert result == expected


# * ---------------------------------------- * #
# * bold_md


@m.parametrize("test_id, args, expected", [("base", ("text",), "**text**")])
def test_bold_md(test_id, args, expected):
    result = wm.bold_md(*args)
    assert result == expected


# ! -------------------------------------------------------------------------------- ! #
# ! API

# * -------------------------------------------------------------------------------- * #
# * RELATIVES

# * ---------------------------------------- * #
# * get_children


@m.parametrize(
    "test_id, args, expected",
    [("root_page", (wm.ROOT_PAGE,), list(WIKI_ROOT.glob(f"*/{wm.PAGE_PATTERN}")))],
)
def test_get_children(test_id, args, expected):
    result = wm.get_children(*args)
    assert result == expected


# * ---------------------------------------- * #
# * get_parent


@m.parametrize(
    "test_id, args, expected",
    [
        ("root_page", (wm.ROOT_PAGE,), WIKI_ROOT / "Home.md"),
        ("subpage", (wm.PAGES[1],), WIKI_ROOT / "Home.md"),
    ],
)
def test_get_parent(test_id, args, expected):
    result = wm.get_parent(*args)
    assert result == expected


# * -------------------------------------------------------------------------------- * #
# * NAVIGATION

# * -------------------------------------------------------------------------------- * #
# * FILE OPERATIONS

# * ---------------------------------------- * #
# * init_page


@m.parametrize(
    "test_id, args",
    [
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
    ],
)
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
        "base",
        ("test-page-name", wm.ROOT_PAGE, 0),
        wm.WIKI_ROOT / "00_test-page-name/test-page-name.md",
    )
]


@m.parametrize("test_id, args, expected", INIT_PAGE_PARAMS)
def test_init_page(test_id, args, expected):
    result = wm.init_page(*args)
    assert result == expected


# * ---------------------------------------- * #
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


# * ---------------------------------------- * #
# * find_page

FIND_PAGE_PARAMS = [
    # (
    #     <test_id>
    #     <args>
    #     <expected>
    # ),
    (
        "root_page",
        (wm.ROOT_PAGE.stem,),
        wm.ROOT_PAGE,
    ),
    (
        "lowercase",
        ("impeach-vermilion-vacuum",),
        FIND_PAGE_LOWERCASE_EXPECTED := (
            WIKI_ROOT / r"00_Impeach-Vermilion-Vacuum\Impeach-Vermilion-Vacuum.md"
        ),
    ),
    (
        "uppercase",
        ("Impeach-Vermilion-Vacuum",),
        FIND_PAGE_LOWERCASE_EXPECTED,
    ),
]


@m.parametrize("test_id, args, expected", FIND_PAGE_PARAMS)
def test_find_page(test_id, args, expected, RESTORE_WIKI_BEFORE_TEST):
    result = wm.find_page(*args)
    assert result == expected


# ! -------------------------------------------------------------------------------- ! #
# ! CLI
