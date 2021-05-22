"""Functions that find the family of a page."""

from __future__ import annotations  # postponed evaluation of annotations

from pathlib import Path

from wikiman import common

PAGE_PATTERN = "[!_]*.md"

# The origin repo should be a GitHub wiki, and pages should be in the "wiki" subfolder
ROOT_NAME = "wiki"
WIKI_ROOT = Path(ROOT_NAME)


def init_wiki(wiki_root: Path = WIKI_ROOT):
    if not WIKI_ROOT.exists():
        WIKI_ROOT.mkdir()
        (WIKI_ROOT / "Home.md").touch()


def get_pages(wiki_root: Path = WIKI_ROOT) -> list[Page]:
    paths = sorted(wiki_root.glob(f"**/{PAGE_PATTERN}"))
    return [Page(path) for path in paths]


class Page:
    def __init__(self, path: Path):
        self.path = path
        self.name = path.stem

    def make(self):
        self.mkdir()
        self.path.touch()

    def mkdir(self):
        if not self.path.exists():
            self.path.mkdir()


# * -------------------------------------------------------------------------------- * #
# * FAMILY


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
