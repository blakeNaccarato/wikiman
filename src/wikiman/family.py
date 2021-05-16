from pathlib import Path

from wikiman import common


def get_siblings(page: Path) -> list[Path]:
    """Get a page and its siblings. The home page has its children as its siblings."""

    parent = get_parent(page)
    siblings = get_children(parent)
    return siblings


def get_parent(page: Path) -> Path:
    """Get the parent of a page."""

    if page == common.ROOT_PAGE:
        # Make the Home page its own parent
        parent = page
    else:
        # Make the page in the parent directory its parent
        page_directory = page.parent
        parent_directory = page_directory.parent
        # If each page has its own directory, glob should get only one page, the parent
        parent = sorted(parent_directory.glob(common.PAGE_PATTERN))[0]

    return parent


def get_children(page: Path) -> list[Path]:
    """Get the children of a page."""

    parent_directory = page.parent
    return sorted(parent_directory.glob(f"*/{common.PAGE_PATTERN}"))
