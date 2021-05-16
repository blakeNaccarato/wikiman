import pytest
from pytest import mark as m
from wikiman import utils

from conftest import WIKI_ROOT
from test_wikiman import PAGES

# ! -------------------------------------------------------------------------------- ! #
# ! UTILITIES


# * ---------------------------------------- * #
# * get_prev


@m.parametrize(
    "test_id, args, expected",
    [
        (
            "is_first_child",
            (
                PAGES["measure-transient-respite"],
                [
                    PAGES["measure-transient-respite"],
                    PAGES["official-union-advantage"],
                    PAGES["middle-pasture-floating"],
                ],
                0,
            ),
            PAGES["impeach-vermilion-vacuum"],
        ),
        (
            "else",
            (
                PAGES["official-union-advantage"],
                [
                    PAGES["measure-transient-respite"],
                    PAGES["official-union-advantage"],
                    PAGES["middle-pasture-floating"],
                ],
                1,
            ),
            PAGES["measure-transient-respite"],
        ),
    ],
)
def test_get_prev(test_id, args, expected):
    result = utils.get_prev(*args)
    assert result == expected


# * ---------------------------------------- * #
# * get_next_of_last_child


@m.parametrize(
    "test_id, args, expected",
    [
        ("is_last_page", (PAGES["reaction-diagonal-patter"],), PAGES["home"]),
        (
            "elif_parent_is_last_child",
            (PAGES["meridian-preserve-winter"],),
            PAGES["equity-substitute-huddle"],
        ),
        (
            "else",
            (PAGES["middle-pasture-floating"],),
            PAGES["equity-substitute-huddle"],
        ),
    ],
)
def test_get_next_of_last_child(test_id, args, expected):
    result = utils.get_next_of_last_child(*args)
    assert result == expected


# * ---------------------------------------- * #
# * get_next


@m.parametrize(
    "test_id, args, expected",
    [
        (
            "has_children",
            (
                PAGES["equity-substitute-huddle"],
                [
                    PAGES["impeach-vermilion-vacuum"],
                    PAGES["equity-substitute-huddle"],
                ],
                1,
            ),
            PAGES["automatic-party-merit"],
        ),
        (
            "elif_is_last_child",
            (
                PAGES["serpentine-hurry-butcher"],
                [
                    PAGES["close-waste-transform"],
                    PAGES["transit-thrum-middle"],
                    PAGES["serpentine-hurry-butcher"],
                ],
                2,
            ),
            PAGES["middle-pasture-floating"],
        ),
        (
            "else",
            (
                PAGES["medium-establish-vital"],
                [
                    PAGES["automatic-party-merit"],
                    PAGES["medium-establish-vital"],
                    PAGES["reaction-diagonal-patter"],
                ],
                1,
            ),
            PAGES["reaction-diagonal-patter"],
        ),
    ],
)
def test_get_next(test_id, args, expected):
    result = utils.get_next(*args)
    assert result == expected


# * -------------------------------------------------------------------------------- * #
# * PAGES

# * ---------------------------------------- * #
# * find_page


@m.parametrize(
    "test_id, args, expected",
    [
        ("home", ("Home",), PAGES["home"]),
        ("lowercase", ("impeach-vermilion-vacuum",), PAGES["impeach-vermilion-vacuum"]),
        ("uppercase", ("Impeach-Vermilion-Vacuum",), PAGES["impeach-vermilion-vacuum"]),
        ("subpage", ("measure-transient-respite",), PAGES["measure-transient-respite"]),
    ],
)
def test_find_page(test_id, args, expected, RESTORE_WIKI):
    result = utils.find_page(*args)
    assert result == expected


@m.parametrize("test_id, args", [("page_not_found", ("Page-That-Doesn't-Exist",))])
def test_find_page_raises(test_id, args, RESTORE_WIKI):
    with pytest.raises(ValueError):
        utils.find_page(*args)


# * ---------------------------------------- * #
# * init_page


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
    result = utils.init_page(*args)
    assert result == expected


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
        utils.init_page(*args)


# * ---------------------------------------- * #
# * get_page_position


@m.parametrize(
    "test_id, args, expected",
    [
        ("home", (PAGES["home"],), 0),
        (0, (PAGES["impeach-vermilion-vacuum"],), 0),
        (1, (PAGES["measure-transient-respite"],), 0),
        (2, (PAGES["middle-pasture-floating"],), 2),
        (3, (PAGES["medium-establish-vital"],), 1),
    ],
)
def test_get_page_position(test_id, args, expected):
    result = utils.get_page_position(*args)
    assert result == expected


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
    result = utils.get_dashed_name(*args)
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
    result = utils.get_human_name(*args)
    assert result == expected


# * ---------------------------------------- * #
# * get_md_name


@m.parametrize(
    "test_id, args, expected", [("base", ("Name of a page",), "Name-of-a-page.md")]
)
def test_get_md_name(test_id, args, expected):
    result = utils.get_md_name(*args)
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
    result = utils.get_dir_name(*args)
    assert result == expected


# * -------------------------------------------------------------------------------- * #
# * MARKDOWN

# * ---------------------------------------- * #
# * get_page_url

# We use `utils.GIT_REMOTE_URL` because we don't care about that part. That will
# resolve the wiki repo properly when invoked by end-users. Sure, it doesn't give us a
# "proper" wiki link in the test suite, since we're not invoking this from a "proper"
# wiki repo. And we can't pytest.fixtures.monkeypatch a module-level variable, either.
@m.parametrize(
    "test_id, args, expected",
    [("base", (PAGES["home"],), utils.GIT_REMOTE_URL + "Home")],
)
def test_get_page_url(test_id, args, expected):
    result = utils.get_page_url(*args)
    assert result == expected


# * ---------------------------------------- * #
# * get_md_link


@m.parametrize("test_id, args, expected", [("base", ("text", "link"), "[text](link)")])
def test_get_md_link(test_id, args, expected):
    result = utils.get_md_link(*args)
    assert result == expected


# * ---------------------------------------- * #
# * get_page_link


@m.parametrize(
    "test_id, args, expected",
    [("base", (PAGES["home"],), f"[Home]({utils.GIT_REMOTE_URL}Home)")],
)
def test_get_page_link(test_id, args, expected):
    result = utils.get_page_link(*args)
    assert result == expected


# * ---------------------------------------- * #
# * bold_md


@m.parametrize("test_id, args, expected", [("base", ("text",), "**text**")])
def test_bold_md(test_id, args, expected):
    result = utils.bold_md(*args)
    assert result == expected
