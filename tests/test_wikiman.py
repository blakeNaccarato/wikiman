# pylint: disable=missing-module-docstring, missing-function-docstring

import wikiman as wm


def test_move_page():

    # TODO

    page = wm.find_page("tour-of-vscode")
    under = wm.find_page("first-time-setup")
    wm.move_page(page, under, 2)
    assert 1
