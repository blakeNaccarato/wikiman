import wikiman as wm
from pytest import mark as m
from wikiman import utils

from test_wikiman import PAGES

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

# We use `utils.GIT_REMOTE_URL` because we don't care about that part. That will
# resolve the wiki repo properly when invoked by end-users. Sure, it doesn't give us a
# "proper" wiki link in the test suite, since we're not invoking this from a "proper"
# wiki repo. And we can't pytest.fixtures.monkeypatch a module-level variable, either.
@m.parametrize(
    "test_id, args, expected",
    [("base", (PAGES["home"],), utils.GIT_REMOTE_URL + "Home")],
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
    [("base", (PAGES["home"],), f"[Home]({utils.GIT_REMOTE_URL}Home)")],
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
