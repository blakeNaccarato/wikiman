from pytest import mark as m
from wikiman import family

from test_wikiman import PAGES

# * ---------------------------------------- * #
# * get_children

PAGE_PATTERN = "[!_]*.md"


@m.parametrize(
    "test_id, args, expected",
    [
        (
            "no_children",
            (PAGES["close-waste-transform"],),
            [],
        ),
        (
            "home",
            (PAGES["home"],),
            [PAGES["impeach-vermilion-vacuum"], PAGES["equity-substitute-huddle"]],
        ),
        (
            0,
            (PAGES["impeach-vermilion-vacuum"],),
            [
                PAGES["measure-transient-respite"],
                PAGES["official-union-advantage"],
                PAGES["middle-pasture-floating"],
            ],
        ),
        (
            1,
            (PAGES["equity-substitute-huddle"],),
            [
                PAGES["automatic-party-merit"],
                PAGES["medium-establish-vital"],
                PAGES["reaction-diagonal-patter"],
            ],
        ),
        (
            2,
            (PAGES["official-union-advantage"],),
            [
                PAGES["close-waste-transform"],
                PAGES["transit-thrum-middle"],
                PAGES["serpentine-hurry-butcher"],
            ],
        ),
    ],
)
def test_get_children(test_id, args, expected):
    result = family.get_children(*args)
    assert result == expected


# * ---------------------------------------- * #
# * get_parent


@m.parametrize(
    "test_id, args, expected",
    [
        ("home", (PAGES["home"],), PAGES["home"]),
        (0, (PAGES["impeach-vermilion-vacuum"],), PAGES["home"]),
        (1, (PAGES["serpentine-hurry-butcher"],), PAGES["official-union-advantage"]),
    ],
)
def test_get_parent(test_id, args, expected):
    result = family.get_parent(*args)
    assert result == expected


# * ---------------------------------------- * #
# * get_siblings


@m.parametrize(
    "test_id, args, expected",
    [
        (
            "home",
            (PAGES["home"],),
            [PAGES["impeach-vermilion-vacuum"], PAGES["equity-substitute-huddle"]],
        ),
        (
            "subpage",
            (PAGES["impeach-vermilion-vacuum"],),
            [PAGES["impeach-vermilion-vacuum"], PAGES["equity-substitute-huddle"]],
        ),
        ("only_child", (PAGES["slate-slide-course"],), [PAGES["slate-slide-course"]]),
    ],
)
def test_get_siblings(test_id, args, expected):
    result = family.get_siblings(*args)
    assert result == expected
