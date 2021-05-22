"""Functions that find the family of a page."""

from __future__ import annotations  # postponed evaluation of annotations

from pathlib import Path

from wikiman import common, utils

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
        self.folder = path.parent

        # FAMILY
        self.parent = self.get_parent()
        self.children = self.get_children()

        # PAGE
        self.position = self.get_position()

    # * ---------------------------------------------------------------------------- * #
    # * FAMILY

    def get_parent(self, root_page: Path = common.ROOT_PAGE) -> Page:
        """Get the parent of a page."""

        if self.path == root_page:
            # Make the Home page its own parent
            parent = self.path
        else:
            # Make the page in the parent directory its parent
            parent_directory = self.folder.parent
            # If each page has its own directory, glob should get only one page, the parent
            parent = sorted(parent_directory.glob(common.PAGE_PATTERN))[0]

        return Page(parent)

    def get_children(self) -> list[Page]:
        """Get the children of a page."""
        children = sorted(self.folder.glob(f"*/{common.PAGE_PATTERN}"))
        return [Page(child) for child in children]

    # * ---------------------------------------------------------------------------- * #
    # * PAGE

    def get_position(self, root_page: Path = common.ROOT_PAGE):
        """Get the position of a page."""

        if self.path == root_page:
            position = 0
        else:
            position = int(self.folder.name.split("_")[0])
        return position

    def init_page(self, under: Page) -> Path:
        """Initialize a page in the wiki."""

        if utils.ILLEGAL_CHARACTERS.search(self.name):
            message = 'Name cannot contain escape sequences or \\ / : * ? " < > |'
            raise ValueError(message)

        destination_dir = under.folder
        page_dir = destination_dir / utils.get_dir_name(self.name, self.position)
        page = page_dir / utils.get_md_name(self.name)
        return page

    # * ---------------------------------------------------------------------------- * #
    # * MAKE

    def make(self):
        self.mkdir()
        self.path.touch()

    def mkdir(self):
        if not self.path.exists():
            self.folder.mkdir()


# * -------------------------------------------------------------------------------- * #
# * PAGE


# def get_page_position(page: Path, root_page: Path = common.ROOT_PAGE) -> int:
#     """Get the position of a page."""

#     if page == root_page:
#         position = 0
#     else:
#         page_dir = page.parent
#         position = int(page_dir.name.split("_")[0])
#     return position


# def init_page(name: str, under: Path, position: int) -> Path:
#     """Initialize a page in the wiki at the specified position."""

#     if utils.ILLEGAL_CHARACTERS.search(name):
#         message = 'Name cannot contain escape sequences or \\ / : * ? " < > |'
#         raise ValueError(message)

#     destination_dir = under.parent
#     page_dir = destination_dir / utils.get_dir_name(name, position)
#     page = page_dir / utils.get_md_name(name)
#     return page


def find_page(name: str, pages: list[Path]) -> Path:
    """Find an existing page."""

    page_names = [utils.get_dashed_name(page.stem).lower() for page in pages]

    try:
        page_location = page_names.index(utils.get_dashed_name(name).lower())
    except ValueError as exception:
        raise ValueError("Page not found.") from exception
    return common.PAGES[page_location]


# * -------------------------------------------------------------------------------- * #
# * FAMILY


def get_siblings(page: Path) -> list[Path]:
    """Get a page and its siblings. The home page has its children as its siblings."""

    parent = get_parent(page)
    siblings = get_children(parent)
    return siblings


def get_parent(page: Path, root_page: Path = common.ROOT_PAGE) -> Path:
    """Get the parent of a page."""

    if page == root_page:
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
