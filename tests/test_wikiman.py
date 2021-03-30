# pylint: disable=missing-module-docstring, missing-function-docstring

import wikiman as wm


def test_test():

    wm.get_page_url("yes")

    # page = wm.find_page("tour-of-vscode")
    # under = wm.find_page("first-time-setup")
    # wm.move_page(page, under, 2)
    assert 1
