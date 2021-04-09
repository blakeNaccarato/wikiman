# pylint: disable=missing-function-docstring, missing-module-docstring, redefined-outer-name, unused-argument, wrong-import-order

from filecmp import dircmp

import pytest
import wikiman as wm
from pytest import mark as m


# * -------------------------------------------------------------------------------- * #
# * FILE OPERATIONS


def test_add_page():
    wm.add_page("Measure-Transient-Respite", "Impeach-Vermilion-Vacuum")


# * -------------------------------------------------------------------------------- * #
# * FILE OPERATIONS


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
        "escapes",
        ("E\as\bc\fa\np\re\ts\v", wm.ROOT_PAGE, 0),
    ),
    (
        "all_others",
        ('/:*?"<>|', wm.ROOT_PAGE, 0),
    ),
]


@m.parametrize("test_id, args", INIT_PAGE_RAISES_PARAMS)
def test_init_page_raises(test_id, args):

    (name, under, position) = args

    with pytest.raises(ValueError):
        wm.init_page(name, under, position)


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

    (name, under, position) = args

    result = wm.init_page(name, under, position)

    assert result == expected


CREATE_PAGE_PARAMS = [param[:2] for param in INIT_PAGE_PARAMS]


@m.parametrize("test_id, args", CREATE_PAGE_PARAMS)
def test_create_page(test_id, args, expected_wiki):

    (name, under, position) = args
    page = wm.init_page(name, under, position)
    wm.create_page(page)

    result = dircmp(wm.WIKI_ROOT, expected_wiki)

    assert not result.diff_files


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
