"""Utility functions."""

import re
from pathlib import Path

import git

from wikiman import common, family

ILLEGAL_CHARACTERS = re.compile(r'[\\/:*?"<>|\a\b\f\n\r\t\v]')

WIDTH = 2  # Width of the number to prepend to directories
GIT_REMOTE_URL = (
    str(git.Repo().remotes.origin.url.removesuffix(".wiki.git")) + "/wiki" + "/"
)


# * -------------------------------------------------------------------------------- * #
# * GET NEAREST


def get_nearest(
    page: Path, root_page: Path = common.ROOT_PAGE
) -> tuple[Path, Path, Path]:
    """Get the pages nearest to a page."""

    siblings = family.get_siblings(page)
    if page == root_page:
        next_page = siblings[0] if siblings else root_page
        prev_page = root_page
    else:
        page_position = siblings.index(page)
        next_page = get_next(page, siblings, page_position)
        prev_page = get_prev(page, siblings, page_position)

    parent = family.get_parent(page)
    return next_page, prev_page, parent


def get_next(page: Path, siblings: list[Path], page_position: int) -> Path:
    """Get the page just after this page."""

    children = family.get_children(page)
    is_last_child = page_position + 1 >= len(siblings)
    if children:
        next_page = children[0]
    elif is_last_child:
        next_page = get_next_of_last_child(page)
    else:
        next_page = siblings[page_position + 1]
    return next_page


def get_next_of_last_child(page: Path, root_page: Path = common.ROOT_PAGE) -> Path:
    """Get the next page of a last child."""

    parent = family.get_parent(page)
    is_last_page = parent == root_page
    if is_last_page:
        next_page = root_page
    else:
        siblings_of_parent = family.get_siblings(parent)
        next_page_position = siblings_of_parent.index(parent) + 1
        parent_is_last_child = next_page_position >= len(siblings_of_parent)
        if parent_is_last_child:
            next_page = get_next_of_last_child(parent)
        else:
            next_page = siblings_of_parent[next_page_position]
    return next_page


def get_prev(page: Path, siblings: list[Path], page_position: int) -> Path:
    """Get the page just before this page."""

    is_first_child = page_position == 0
    return family.get_parent(page) if is_first_child else siblings[page_position - 1]


# * -------------------------------------------------------------------------------- * #
# * PAGE


def get_page_position(page: Path, root_page: Path = common.ROOT_PAGE) -> int:
    """Get the position of a page."""

    if page == root_page:
        position = 0
    else:
        page_dir = page.parent
        position = int(page_dir.name.split("_")[0])
    return position


def init_page(name: str, under: Path, position: int) -> Path:
    """Initialize a page in the wiki at the specified position."""

    if ILLEGAL_CHARACTERS.search(name):
        message = 'Name cannot contain escape sequences or \\ / : * ? " < > |'
        raise ValueError(message)

    destination_dir = under.parent
    page_dir = destination_dir / get_dir_name(name, position)
    page = page_dir / get_md_name(name)
    return page


def find_page(name: str, pages: list[Path]) -> Path:
    """Find an existing page."""

    page_names = [get_dashed_name(page.stem).lower() for page in pages]

    try:
        page_location = page_names.index(get_dashed_name(name).lower())
    except ValueError as exception:
        raise ValueError("Page not found.") from exception
    return common.PAGES[page_location]


# * -------------------------------------------------------------------------------- * #
# * MARKDOWN


def bold_md(text: str) -> str:
    """Make text bold in Markdown format."""

    return f"**{text}**"


def get_page_link(page: Path) -> str:
    """Get a link to a page in Markdown format."""

    return get_md_link(get_human_name(page.stem), get_page_url(page))


def get_md_link(text: str, link: str) -> str:
    """Get a link in Markdown format."""

    return f"[{text}]({link})"


def get_page_url(page: Path) -> str:
    """Get the URL for a page."""

    return GIT_REMOTE_URL + page.stem


# * -------------------------------------------------------------------------------- * #
# * STRINGS


def get_dir_name(name: str, index: int) -> str:
    """Get the name for the directory containing a page in the file structure."""

    return str(index).zfill(WIDTH) + "_" + get_dashed_name(name)


def get_md_name(name: str) -> str:
    """Get the name for a `*.md` page in the file structure."""

    return get_dashed_name(name) + ".md"


def get_human_name(name: str) -> str:
    """Get a human-readable name."""

    return name.replace("-", " ")


def get_dashed_name(name: str) -> str:
    """Get a dashed name."""

    return name.replace(" ", "-")
