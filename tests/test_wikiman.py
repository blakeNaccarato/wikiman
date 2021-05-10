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
    "Measure-Transient-Respite": (MEASURE := IMPEACH / "00_Measure-Transient-Respite"),
    # >>> Under "Measure..."
    "Slate-Slide-Course": (SLATE := (MEASURE / "00_Slate-Slide-Course")),
    # >>>> Under "Slate..."
    "Height-Collar-Detail": (SLATE / "00_Height-Collar-Detail"),
    # >> Under "Impeach..."
    "Official-Union-Advantage": (OFFICIAL := IMPEACH / "01_Official-Union-Advantage"),
    # >>> Under "Official..."
    "Close-Waste-Transform": OFFICIAL / "00_Close-Waste-Transform",
    "Transit-Thrum-Middle": (TRANSIT := OFFICIAL / "01_Transit-Thrum-Middle"),
    # >>>> Under "Transit..."
    "Knuckle-Conversion-Wound": TRANSIT / "00_Knuckle-Conversion-Wound",
    "Serpentine-Hurry-Butcher": OFFICIAL / "02_Serpentine-Hurry-Butcher",
    # >> Under "Impeach..."
    "Middle-Pasture-Floating": (MIDDLE := IMPEACH / "02_Middle-Pasture-Floating"),
    # >>> Under "Middle..."
    "Meridian-Preserve-Winter": MIDDLE / "00_Meridian-Preserve-Winter",
    # > Under "Home"
    "Equity-Substitute-Huddle": (EQUITY := WIKI_ROOT / "01_Equity-Substitute-Huddle"),
    # >> Under "Equity.."
    "Automatic-Party-Merit": EQUITY / "00_Automatic-Party-Merit",
    "Medium-Establish-Vital": EQUITY / "01_Medium-Establish-Vital",
    "Reaction-Diagonal-Patter": EQUITY / "02_Reaction-Diagonal-Patter",
}

PAGES = {str(key).lower(): value / (key + ".md") for key, value in PAGE_PATHS.items()}

# # ! -------------------------------------------------------------------------------- ! #
# # ! UTILITIES

# # * -------------------------------------------------------------------------------- * #
# # * PAGES

# # * ---------------------------------------- * #
# # * find_page


# @m.parametrize(
#     "test_id, args, expected",
#     [
#         ("home", ("Home",), PAGES["home"]),
#         ("lowercase", ("impeach-vermilion-vacuum",), PAGES["impeach-vermilion-vacuum"]),
#         ("uppercase", ("Impeach-Vermilion-Vacuum",), PAGES["impeach-vermilion-vacuum"]),
#         ("subpage", ("measure-transient-respite",), PAGES["measure-transient-respite"]),
#     ],
# )
# def test_find_page(test_id, args, expected, RESTORE_WIKI):
#     result = wm.find_page(*args)
#     assert result == expected


# @m.parametrize("test_id, args", [("page_not_found", ("Page-That-Doesn't-Exist",))])
# def test_find_page_raises(test_id, args, RESTORE_WIKI):
#     with pytest.raises(ValueError):
#         wm.find_page(*args)


# # * ---------------------------------------- * #
# # * init_page


# INIT_PAGE_PARAMS = [
#     # (
#     #     <test_id>
#     #     <args>
#     #     <expected>
#     # ),
#     (
#         "base",
#         ("test-page-name", PAGES["home"], 0),
#         WIKI_ROOT / "00_test-page-name/test-page-name.md",
#     )
# ]


# @m.parametrize("test_id, args, expected", INIT_PAGE_PARAMS)
# def test_init_page(test_id, args, expected):
#     result = wm.init_page(*args)
#     assert result == expected


# @m.parametrize(
#     "test_id, args",
#     [
#         ("backslash", (r"Backs\lash", PAGES["home"], 0)),
#         ("escape_sequences", ("E\as\bc\fa\np\re\ts\v", PAGES["home"], 0)),
#         ("all_others", ('/:*?"<>|', PAGES["home"], 0)),
#     ],
# )
# def test_init_page_raises(test_id, args):
#     with pytest.raises(ValueError):
#         wm.init_page(*args)


# # * ---------------------------------------- * #
# # * get_page_position


# @m.parametrize(
#     "test_id, args, expected",
#     [
#         ("home", (PAGES["home"],), 0),
#         (0, (PAGES["impeach-vermilion-vacuum"],), 0),
#         (1, (PAGES["measure-transient-respite"],), 0),
#         (2, (PAGES["middle-pasture-floating"],), 2),
#         (3, (PAGES["medium-establish-vital"],), 1),
#     ],
# )
# def test_get_page_position(test_id, args, expected):
#     result = wm.get_page_position(*args)
#     assert result == expected


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
    result = wm.get_children(*args)
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
    result = wm.get_parent(*args)
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
    result = wm.get_siblings(*args)
    assert result == expected


# * -------------------------------------------------------------------------------- * #
# * RELATIVES


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
    result = wm.get_prev(*args)
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
    result = wm.get_next_of_last_child(*args)
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
    result = wm.get_next(*args)
    assert result == expected


# * ---------------------------------------- * #
# * get_nearest


@m.parametrize(
    "test_id, args, expected",
    [
        (
            "home",
            (PAGES["home"],),
            (PAGES["impeach-vermilion-vacuum"], PAGES["home"], PAGES["home"]),
        ),
        # (
        #     #? Can't test this path without a lot of fixturing
        #     "home_is_only_page",
        #     (PAGES["home"],),
        #     (PAGES["home"], PAGES["home"], PAGES["home"]),
        # ),
        (
            "else",
            (PAGES["medium-establish-vital"],),
            (
                PAGES["reaction-diagonal-patter"],
                PAGES["automatic-party-merit"],
                PAGES["equity-substitute-huddle"],
            ),
        ),
    ],
)
def test_get_nearest(test_id, args, expected):
    result = wm.get_nearest(*args)
    assert result == expected


# * -------------------------------------------------------------------------------- * #
# * NAVIGATION

# * -------------------------------------------------------------------------------- * #
# * FILE OPERATIONS


# # * ---------------------------------------- * #
# # * create_page

# # reuse params from init_page, but compare to `expected_wiki` instead of `expected`
# CREATE_PAGE_PARAMS = [param[:2] for param in INIT_PAGE_PARAMS]


# @m.parametrize("test_id, args", CREATE_PAGE_PARAMS)
# def test_create_page(test_id, args, EXPECTED_WIKI):

#     page = wm.init_page(*args)

#     wm.create_page(page)
#     result = dircmp(WIKI_ROOT, EXPECTED_WIKI)

#     assert not result.diff_files


# ! -------------------------------------------------------------------------------- ! #
# ! CLI
