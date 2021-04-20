"""Generate wiki navigation links in the sidebar and footer of each page."""

import itertools
import re
from pathlib import Path
from typing import Optional

import fire
import git
from markdown import Markdown

# Patterns specific to GitHub Wiki
PAGE_PATTERN = "[!_]*.md"
SIDEBAR_FILENAME = "_Sidebar.md"
FOOTER_FILENAME = "_Footer.md"
ILLEGAL_CHARACTERS = re.compile(r'[\\/:*?"<>|\a\b\f\n\r\t\v]')

# The origin repo should be a GitHub wiki, and pages should be in the "wiki" subfolder
ROOT_NAME = "wiki"
GIT_REMOTE_URL = git.Repo().remotes.origin.url.removesuffix(".wiki.git") + "/wiki" + "/"

# Get pages to be used throughout the module
WIKI_ROOT = Path(ROOT_NAME)

if not WIKI_ROOT.exists():
    WIKI_ROOT.mkdir()
    (WIKI_ROOT / "Home.md").touch()

PAGES = list(sorted(WIKI_ROOT.glob(f"**/{PAGE_PATTERN}")))
ROOT_PAGE = PAGES[-1]

# Glyphs to place in the footer next to "Up", "Prev", and "Next" navigation links.
NAV_HEAD = ("Next: ", "Prev: ", "Up: ")
# Heading levels indicated by number of "#" in sequence. Changes header size.
MD_HEAD = "# "
# Two newlines signifies a paragraph break in Markdown.
MD_NEWLINE = "  \n"
# Workaround. Markdown converts sequential whitespace (other than \n) to single spaces.
MD_TAB = "&nbsp;" * 4
# Width of the number to prepend to directories
WIDTH = 2


def main():
    """The command-line interface. Runs if file is invoked directly, or from prompt."""

    fire.Fire({"up": cli_update_navigation, "add": cli_add_page})


# ! -------------------------------------------------------------------------------- ! #
# ! CLI


def cli_update_navigation():
    """Update sidebars and footers."""

    for page in PAGES:

        # Write the tree of nearby pages and the TOC for this page into the sidebar
        tree = get_tree(page)
        toc = get_toc(page)
        sidebar_text = MD_NEWLINE.join(
            [f"{MD_HEAD}Directory", tree, f"{MD_HEAD}Contents", toc]
        )
        sidebar = page.parent / SIDEBAR_FILENAME
        with open(sidebar, "w") as file:
            file.write(sidebar_text)

        # Write relative navigation links into the footer
        nav = get_relative_nav(page)
        footer = page.parent / FOOTER_FILENAME
        with open(footer, "w") as file:
            file.write(nav)


def cli_add_page(name: str, under: str, position: Optional[int] = None):
    """Add a new page under a page, optionally specifying position."""

    parent = find_page(under)

    if position is None:
        position = len(get_children(parent))
    else:
        # Get the children that will come after the new page
        children = get_children(parent)
        children_after = children[position:]

        # Shift child directory numbering to accomdate the new page
        for child in children_after:
            new_child_position = get_page_position(child) + 1
            move_page(child, parent, new_child_position)

    page = init_page(name, parent, position)
    create_page(page)


# def cli_move_page():  # name: str, under: str, position: Optional[int] = None):
#     """Move a page under a page, optionally specifying position."""

#     pass


# ! -------------------------------------------------------------------------------- ! #
# ! API


# * -------------------------------------------------------------------------------- * #
# * FILE OPERATIONS


# def shift_page():  # page: Path, count: int):
#     """Shift a page."""
#     pass


def move_page(page: Path, under: Path, position: int):
    """Change the position of a page."""

    new_page = init_page(page.stem, under, position)
    new_page.parent.mkdir()
    page.rename(new_page)


def remove_page(page: Path):
    """Remove a page."""

    page_dir = page.parent
    page.unlink()
    for file in [SIDEBAR_FILENAME, FOOTER_FILENAME]:
        (page_dir / file).unlink(missing_ok=True)
    page_dir.rmdir()


def create_page(page: Path):
    """Create a page that has been initialized but does not exist yet."""

    page.parent.mkdir()
    page.touch()


# * -------------------------------------------------------------------------------- * #
# * NAVIGATION


def get_tree(page: Path) -> str:
    """Get Markdown links for the tree of pages near a page."""

    # Start the tree at root or with the page and its siblings
    if page == ROOT_PAGE:
        # Tree is a list of just the root page
        tree = [bold_md(get_page_link(page))]
        page_idx = 0
    else:
        siblings = get_siblings(page)
        tree = [get_page_link(page) for page in siblings]
        page_idx = siblings.index(page)
        tree[page_idx] = bold_md(tree[page_idx])

    # Insert child links below the page
    children = get_children(page)
    child_links = [get_page_link(page) for page in children]
    tree = insert_subtree(subtree=child_links, tree=tree, index=page_idx)

    # Only worry about parents if it's not the root page
    if page != ROOT_PAGE:

        parent = get_parent(page)

        if parent == ROOT_PAGE:
            # Insert the working tree below the root page
            parent_links = [get_page_link(parent)]
            parent_idx = 0
            tree = insert_subtree(subtree=tree, tree=parent_links, index=parent_idx)
        else:
            # Insert the working tree below the parent page in the list of parents
            parents = get_siblings(parent)
            parent_links = [get_page_link(page) for page in parents]
            parent_idx = parents.index(parent)
            tree = insert_subtree(subtree=tree, tree=parent_links, index=parent_idx)

    return MD_NEWLINE.join(tree)


def insert_subtree(subtree: list[str], tree: list[str], index: int):
    """Insert a subtree into a tree after the specified index."""

    index += 1  # To insert *after* the specified index.

    subtree = [MD_TAB + str(i) for i in subtree]
    tree = list(itertools.chain(tree[:index], subtree, tree[index:]))
    return tree


def get_toc(page: Path) -> str:
    """Get the table of contents for a page."""

    toc_list: list[str] = []
    page_url = get_page_url(page)

    with open(page) as file:
        content = file.read()
        md = Markdown(extensions=["toc"])
        md.convert(content)

    for token in md.toc_tokens:  # type: ignore  # pylint: disable=no-member
        token_id = token["id"]
        name = token["name"]
        link = get_md_link(name, f"{page_url}#{token_id}")
        toc_list.append(link)

    toc = MD_NEWLINE.join(toc_list)

    return toc


def get_relative_nav(page: Path) -> str:
    """Get the parent, previous, and next Markdown links."""

    (next_page, prev_page, parent) = get_nearest(page)
    relative_nav: list[str] = []

    # Get next link for any page except the last page in the entire wiki
    if next_page == ROOT_PAGE:
        next_link = None
    else:
        next_link = get_page_link(next_page)
        relative_nav.append(NAV_HEAD[0] + next_link)

    # Get previous link for any page except the home page
    if page == ROOT_PAGE:
        prev_link = None
    else:
        prev_link = get_page_link(prev_page)
        relative_nav.append(NAV_HEAD[1] + prev_link)

    # Get parent link for any page except for Home, or the first page in a section
    if page == ROOT_PAGE or prev_page == parent:
        parent_link = None
    else:
        parent_link = get_page_link(parent)
        relative_nav.append(NAV_HEAD[2] + parent_link)

    return MD_TAB.join(relative_nav)


# * -------------------------------------------------------------------------------- * #
# * GET NEAREST


def get_nearest(page: Path) -> tuple[Path, Path, Path]:
    """Get the pages nearest to a page."""

    siblings = get_siblings(page)
    if page == ROOT_PAGE:
        if len(siblings) == 0:
            next_page = ROOT_PAGE
        else:
            next_page = siblings[0]
        prev_page = page
    else:
        page_position = siblings.index(page)
        next_page = get_next(page, siblings, page_position)
        prev_page = get_prev(page, siblings, page_position)

    parent = get_parent(page)
    return next_page, prev_page, parent


def get_next(page: Path, siblings: list[Path], page_position: int) -> Path:
    """Get the page just after this page."""

    children = get_children(page)
    has_children = len(children) > 0
    is_last_child = page_position + 1 >= len(siblings)
    if has_children:
        next_page = children[0]
    elif is_last_child:
        next_page = get_next_of_last_child(page)
    else:
        next_page = siblings[page_position + 1]
    return next_page


def get_next_of_last_child(page) -> Path:
    """Get the next page of a last child."""

    parent = get_parent(page)
    is_last_page = parent == ROOT_PAGE
    if is_last_page:
        next_page = ROOT_PAGE
    else:
        siblings_of_parent = get_siblings(parent)
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
    if is_first_child:
        prev_page = get_parent(page)
    else:
        prev_page = siblings[page_position - 1]
    return prev_page


# * -------------------------------------------------------------------------------- * #
# * RELATIVES


def get_siblings(page: Path) -> list[Path]:
    """Get a page and its siblings. The home page has its children as its siblings."""

    parent = get_parent(page)
    children_of_parent = get_children(parent)
    siblings = children_of_parent
    return siblings


def get_parent(page: Path) -> Path:
    """Get the parent of a page."""

    if page == ROOT_PAGE:
        # Make the Home page its own parent
        parent = page

    else:
        # Make the page in the parent directory its parent
        page_directory = page.parent
        parent_directory = page_directory.parent
        # If each page has its own directory, glob should get only one page
        parent = list(sorted(parent_directory.glob(PAGE_PATTERN)))[0]

    return parent


def get_children(page: Path) -> list[Path]:
    """Get the children of a page."""

    parent_directory = page.parent
    return list(sorted(parent_directory.glob(f"*/{PAGE_PATTERN}")))


# ! -------------------------------------------------------------------------------- ! #
# ! UTILITIES


# * -------------------------------------------------------------------------------- * #
# * PAGE


def get_page_position(page: Path) -> int:
    """Get the position of a page."""

    if page == ROOT_PAGE:
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

    page_names = [get_dashed_name(page.stem).lower() for page in PAGES]

    try:
        page_location = page_names.index(get_dashed_name(name).lower())
    except ValueError as exception:
        raise ValueError("Page not found.") from exception
    return PAGES[page_location]


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


# ! -------------------------------------------------------------------------------- ! #
# ! RUN MAIN

if __name__ == "__main__":
    main()
