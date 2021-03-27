"""GitHub Wiki CLI manager."""

import itertools
from pathlib import Path
from typing import Optional

from markdown import Markdown

ROOT_DIRNAME = "wiki"
ROOT_PAGE_NAME = "Home.md"
ROOT_PAGE = Path(ROOT_DIRNAME) / ROOT_PAGE_NAME
PAGE_PATTERN = "[!_]*.md"

WIKI_ROOT = "https://github.com/blakeNaccarato/python-challenges/wiki"

SIDEBAR_FILENAME = "_Sidebar.md"
FOOTER_FILENAME = "_Footer.md"

# Glyphs to place in the footer next to "Up", "Prev", and "Next" navigation links.
NAV_HEAD = ("Up: ", "Prev: ", "Next: ")
# Heading levels indicated by number of "#" in sequence. Changes header size.
MD_HEAD = "# "
# Two newlines signifies a paragraph break in Markdown.
MD_NEWLINE = "  \n"
# Workaround. Markdown converts sequential whitespace (other than \n) to single spaces.
MD_TAB = "&nbsp;" * 4


def main():
    """Runs only if this file is run directly, rather than imported."""

    print("working")


# * -------------------------------------------------------------------------------- * #
# * CLI


def up():
    """Update sidebars and footers."""

    root = Path(ROOT_DIRNAME)
    pages = get_descendants(root)

    for page in pages:

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
        nav = get_relative_nav(page, NAV_HEAD)
        footer = page.parent / FOOTER_FILENAME
        with open(footer, "w") as file:
            file.write(nav)


def add(name: str, after: Optional[str] = None, under: Optional[str] = None):
    """Add a new page after the specified page."""

    root = Path(ROOT_DIRNAME)
    pages = get_descendants(root)
    page_names = [get_md_name(page).lower() for page in pages]

    if after is not None:
        after = after.lower()
        idx = page_names.index(after)
        page = pages[idx]
        parent_directory = get_parent(page).parent
        siblings = get_siblings(page)
        assert True
        # TODO
    elif under is not None:
        pass


# * -------------------------------------------------------------------------------- * #
# * NAVIGATION TEXT ELEMENTS


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

    subtree = [f"{MD_TAB}{i}" for i in subtree]
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


def get_relative_nav(page: Path, nav_head: tuple[str, str, str]) -> str:
    """Get the parent, previous, and next Markdown links."""

    relative_nav: list[str] = []

    nearest_family = get_nearest_family(page)
    (parent, prev_sibling, next_sibling) = nearest_family

    # Get parent link for any page except for Home
    if page == ROOT_PAGE:
        parent_link = None
    else:
        parent_link = get_page_link(parent)
        relative_nav.append(f"{nav_head[0]}{parent_link}")

    # Get previous link for pages with a different previous sibling than their parent
    if parent == prev_sibling:
        prev_link = None
    else:
        prev_link = get_page_link(prev_sibling)
        relative_nav.append(f"{nav_head[1]}{prev_link}")

    # Get next link
    next_link = get_page_link(next_sibling)
    relative_nav.append(f"{nav_head[2]}{next_link}")

    nav = MD_TAB.join(relative_nav)

    return nav


# * -------------------------------------------------------------------------------- * #
# * MARKDOWN


def bold_md(text: str) -> str:
    """Make text bold in Markdown format."""

    return f"**{text}**"


def get_page_link(page: Path) -> str:
    """Get a link to a page in Markdown format."""

    return get_md_link(get_md_name(page), get_page_url(page))


def get_md_link(text: str, link: str) -> str:
    """Get a link in Markdown format."""

    return f"[{text}]({link})"


def get_md_name(page: Path) -> str:
    """Get the human-readable name for a page, as in Markdown."""

    return page.stem.replace("-", " ")


def get_page_url(page: Path) -> str:
    """Get the URL for a page."""

    return f"{WIKI_ROOT}/{page.stem}"


# * -------------------------------------------------------------------------------- * #
# * FAMILY


def get_descendants(page: Path) -> list[Path]:
    """Get a page and all of its descendants."""

    return list(page.glob(f"**/{PAGE_PATTERN}"))


def get_nearest_family(page: Path) -> tuple[Path, Path, Path]:
    """Get a page's parent and its nearest siblings."""

    parent = get_parent(page)
    siblings = get_siblings(page)

    if page.name == ROOT_PAGE_NAME:
        prev_sibling = page  # The Home page is its own previous sibling
        next_sibling = siblings[0]  # The next page is its next sibling
    else:
        page_position = siblings.index(page)

        # Get the previous sibling
        is_first_child = page_position == 0
        if is_first_child:
            prev_sibling = get_parent(page)
        else:
            prev_sibling = siblings[page_position - 1]

        # Get the next sibling
        any_subpages = any(item.is_dir() for item in page.parent.iterdir())
        is_last_child = page_position == len(siblings) - 1
        if any_subpages:
            # Make a page with children have its first child as a sibling
            first_child_dir = [p for p in page.parent.iterdir() if p.is_dir()][0]
            first_child = list(first_child_dir.glob(PAGE_PATTERN))[0]
            next_sibling = first_child
        elif is_last_child:
            # Make the next sibling of the parent also the next sibling of this page
            (*_, next_sibling_of_parent) = get_nearest_family(parent)
            next_sibling = next_sibling_of_parent
        else:
            next_sibling = siblings[page_position + 1]

    return parent, prev_sibling, next_sibling


def get_siblings(page: Path) -> list[Path]:
    """Get a page and its siblings."""

    parent = get_parent(page)
    children_of_parent = get_children(parent)
    siblings = children_of_parent
    return siblings


def get_children(page: Path) -> list[Path]:
    """Get the children of a page."""

    parent_directory = page.parent
    return list(parent_directory.glob(f"*/{PAGE_PATTERN}"))


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
        parent = list(parent_directory.glob(PAGE_PATTERN))[0]

    return parent


# * -------------------------------------------------------------------------------- * #
# * RUN MAIN

if __name__ == "__main__":
    main()
