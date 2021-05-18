from typing import Optional

import fire

from wikiman import common, utils
from wikiman import api


def main() -> None:
    """The command-line interface. Runs if file is invoked directly, or from prompt."""

    fire.Fire({"up": update_navigation, "add": add_page})


def update_navigation() -> None:
    """Update sidebars and footers."""

    # Heading levels indicated by number of "#" in sequence. Changes header size.
    md_head = "# "

    for page in common.PAGES:

        # Write the tree of nearby pages and the TOC for this page into the sidebar
        tree = api.get_tree(page)
        toc = api.get_toc(page)
        sidebar_text = common.MD_NEWLINE.join(
            [f"{md_head}Directory", tree, f"{md_head}Contents", toc]
        )
        sidebar = page.parent / common.SIDEBAR_FILENAME
        with open(sidebar, "w") as file:
            file.write(sidebar_text)

        # Write relative navigation links into the footer
        nav = api.get_relative_nav(page)
        footer = page.parent / common.FOOTER_FILENAME
        with open(footer, "w") as file:
            file.write(nav)


def add_page(name: str, under: str, position: Optional[int] = None) -> None:
    """Add a new page under a page, optionally specifying position."""

    parent = utils.find_page(under)

    if position is None:
        position = len(api.family.get_children(parent))
    else:
        # Get the children that will come after the new page
        children = api.family.get_children(parent)
        children_after = children[position:]

        # Shift child directory numbering to accomdate the new page
        for child in children_after:
            new_child_position = utils.get_page_position(child) + 1
            api.move_page(child, parent, new_child_position)

    page = utils.init_page(name, parent, position)
    api.create_page(page)


# def cli_move_page():  # name: str, under: str, position: Optional[int] = None):
#     """Move a page under a page, optionally specifying position."""

#     pass

# ! -------------------------------------------------------------------------------- ! #
# ! RUN MAIN

if __name__ == "__main__":
    main()
