# pylint: disable=missing-module-docstring, missing-function-docstring, unused-argument, wrong-import-order

import wikiman as wm
from pytest import mark as m


# * -------------------------------------------------------------------------------- * #
# * FILE OPERATIONS


@m.parametrize(
    "test_id, args, expected",
    [
        (
            "name_has_dashes",
            ("test-page-name", wm.ROOT_PAGE, 0),
            wm.ROOT / "00_test-page-name/test-page-name.md",
        ),
        (
            "name_has_spaces",
            ("test page name", wm.ROOT_PAGE, 0),
            wm.ROOT / "00_test-page-name/test-page-name.md",
        ),
    ],
)
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
            wm.ROOT / "Home.md",
        ),
    ],
)
def test_get_parent(test_id, args, expected):

    (page) = args

    result = wm.get_parent(page)

    assert result == expected
