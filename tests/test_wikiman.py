# pylint: disable=missing-function-docstring, missing-module-docstring, redefined-outer-name, unused-argument, wrong-import-order

import pytest
import wikiman as wm
from pytest import mark as m

from conftest import WIKI_ROOT

# We hardcode our expected pages rather than pulling from the module under test. This
# leads to some repetition, but avoids dependencies on module-level variables of the
# module under test. We can map our "expected" results to this hardcoded set of pages
# rather than burying a dependency to the module under test.
PAGE_PATHS = {
    # <name> : <path>
    "Home": WIKI_ROOT,
    # > Under "Home"
    "Impeach-Vermilion-Vacuum": (IMPEACH := WIKI_ROOT / "00_Impeach-Vermilion-Vacuum"),
    # >> Under "Impeach..."
    "Measure-Transient-Respite": IMPEACH / "00_Measure-Transient-Respite",
    "Official-Union-Advantage": (OFFICIAL := IMPEACH / "01_Official-Union-Advantage"),
    # >>> Under "Official..."
    "Close-Waste-Transform": OFFICIAL / "00_Close-Waste-Transform",
    "Transit-Thrum-Middle": OFFICIAL / "01_Transit-Thrum-Middle",
    "Serpentine-Harry-Butcher": OFFICIAL / "02_Serpentine-Harry-Butcher",
    # >> Under "Impeach..."
    "Middle-Pasture-Floating": IMPEACH / "02_Middle-Pasture-Floating",
    # > Under "Home"
    "Equity-Substitute-Huddle": (EQUITY := WIKI_ROOT / "01_Equity-Substitute-Huddle"),
    # >> Under "Equity.."
    "Automatic-Party-Merit": EQUITY / "00_Automatic-Party-Merit",
    "Medium-Establish-Vital": EQUITY / "01_Medium-Establish-Vital",
}

PAGES = {str(key).lower(): value / (key + ".md") for key, value in PAGE_PATHS.items()}

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
    "test_id, args, expected", [("base", (PAGES["home"],), wm.GIT_REMOTE_URL + "Home")]
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
    [("base", (PAGES["home"],), f"[Home]({wm.GIT_REMOTE_URL}Home)")],
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


# * -------------------------------------------------------------------------------- * #
# * PAGES

# * ---------------------------------------- * #
# * find_page


@m.parametrize("test_id, args", [("page_not_found", ("Page-That-Doesn't-Exist",))])
def test_find_page_raises(test_id, args, RESTORE_WIKI_BEFORE_TEST):
    with pytest.raises(ValueError):
        wm.find_page(*args)


@m.parametrize(
    "test_id, args, expected",
    [
        ("root_page", ("Home",), PAGES["home"]),
        ("lowercase", ("impeach-vermilion-vacuum",), PAGES["impeach-vermilion-vacuum"]),
        ("uppercase", ("Impeach-Vermilion-Vacuum",), PAGES["impeach-vermilion-vacuum"]),
    ],
)
def test_find_page(test_id, args, expected, RESTORE_WIKI_BEFORE_TEST):
    result = wm.find_page(*args)
    assert result == expected


# * ---------------------------------------- * #
# * init_page


@m.parametrize(
    "test_id, args",
    [
        ("backslash", (r"Backs\lash", PAGES["home"], 0)),
        ("escape_sequences", ("E\as\bc\fa\np\re\ts\v", PAGES["home"], 0)),
        ("all_others", ('/:*?"<>|', PAGES["home"], 0)),
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
        ("test-page-name", PAGES["home"], 0),
        WIKI_ROOT / "00_test-page-name/test-page-name.md",
    )
]


@m.parametrize("test_id, args, expected", INIT_PAGE_PARAMS)
def test_init_page(test_id, args, expected):
    result = wm.init_page(*args)
    assert result == expected


# # * ---------------------------------------- * #
# # * create_page

# # reuse params from init_page, but compare to `expected_wiki` instead of `expected`
# CREATE_PAGE_PARAMS = [param[:2] for param in INIT_PAGE_PARAMS]


# @m.parametrize("test_id, args", CREATE_PAGE_PARAMS)
# def test_create_page(test_id, args, EXPECTED_WIKI):

#     # TODO: Implement EXPECTED_WIKI for parametrized tests

#     page = wm.init_page(*args)

#     wm.create_page(page)
#     result = dircmp(WIKI_ROOT, EXPECTED_WIKI)

#     assert not result.diff_files


# ! -------------------------------------------------------------------------------- ! #
# ! API

# * -------------------------------------------------------------------------------- * #
# * RELATIVES

# * ---------------------------------------- * #
# * get_children

PAGE_PATTERN = "[!_]*.md"


@m.parametrize(
    "test_id, args, expected",
    [
        (
            "root_page",
            (PAGES["home"],),
            [PAGES["impeach-vermilion-vacuum"], PAGES["equity-substitute-huddle"]],
        )
    ],
)
def test_get_children(test_id, args, expected):
    result = wm.get_children(*args)
    assert result == expected


# * ---------------------------------------- * #
# * get_parent


@m.parametrize(
    "test_id, args, expected",
    [
        ("root_page", (PAGES["home"],), PAGES["home"]),
        ("subpage", (wm.find_page("impeach-vermilion-vacuum"),), PAGES["home"]),
    ],
)
def test_get_parent(test_id, args, expected):
    result = wm.get_parent(*args)
    assert result == expected


# * ---------------------------------------- * #
# * get_siblings

GET_SIBLINGS_PARAMS = [
    (
        "root_page",
        (PAGES["home"],),
        EXPECTED_SIBLINGS := [
            PAGES["impeach-vermilion-vacuum"],
            PAGES["equity-substitute-huddle"],
        ],
    ),
    ("subpage", (PAGES["impeach-vermilion-vacuum"],), EXPECTED_SIBLINGS),
]


@m.parametrize("test_id, args, expected", GET_SIBLINGS_PARAMS)
def test_get_siblings(test_id, args, expected):
    result = wm.get_siblings(*args)
    assert result == expected


# * -------------------------------------------------------------------------------- * #
# * NAVIGATION

# * -------------------------------------------------------------------------------- * #
# * FILE OPERATIONS


# ! -------------------------------------------------------------------------------- ! #
# ! CLI
