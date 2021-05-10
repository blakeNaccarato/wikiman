"""Utility functions."""

import re
from pathlib import Path

import git

from wikiman import common

ILLEGAL_CHARACTERS = re.compile(r'[\\/:*?"<>|\a\b\f\n\r\t\v]')

WIDTH = 2  # Width of the number to prepend to directories
GIT_REMOTE_URL = (
    str(git.Repo().remotes.origin.url.removesuffix(".wiki.git")) + "/wiki" + "/"
)

# * -------------------------------------------------------------------------------- * #
# * PAGE


def get_page_position(page: Path) -> int:
    """Get the position of a page."""

    if page == common.ROOT_PAGE:
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


def find_page(name: str) -> Path:
    """Find an existing page."""

    page_names = [get_dashed_name(page.stem).lower() for page in common.PAGES]

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