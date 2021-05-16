"""Generate wiki navigation links in the sidebar and footer of each page."""

from pathlib import Path

from markdown import Markdown

from wikiman import common, family, utils

# ! -------------------------------------------------------------------------------- ! #
# ! API


# * -------------------------------------------------------------------------------- * #
# * FILE OPERATIONS


# def shift_page():  # page: Path, count: int):
#     """Shift a page."""
#     pass


def move_page(page: Path, under: Path, position: int) -> None:
    """Change the position of a page."""

    new_page = utils.init_page(page.stem, under, position)
    new_page.parent.mkdir()
    page.rename(new_page)


def remove_page(page: Path) -> None:
    """Remove a page."""

    page_dir = page.parent
    page.unlink()
    for file in [common.SIDEBAR_FILENAME, common.FOOTER_FILENAME]:
        (page_dir / file).unlink(missing_ok=True)
    page_dir.rmdir()


def create_page(page: Path) -> None:
    """Create a page that has been initialized but does not exist yet."""

    page.parent.mkdir()
    page.touch()


# * -------------------------------------------------------------------------------- * #
# * NAVIGATION

# Workaround. Markdown converts sequential whitespace (other than \n) to single spaces.
MD_TAB = "&nbsp;" * 4


def get_tree(page: Path) -> str:
    """Get Markdown links for the tree of pages near a page."""

    # Start the tree at root or with the page and its siblings
    if page == common.ROOT_PAGE:
        # Tree is a list of just the root page
        tree = [utils.bold_md(utils.get_page_link(common.ROOT_PAGE))]
        page_idx = 0
    else:
        # Tree is a list of the page and its siblings
        siblings = family.get_siblings(page)
        tree = [utils.get_page_link(page) for page in siblings]
        page_idx = siblings.index(page)
        tree[page_idx] = utils.bold_md(tree[page_idx])

    # Insert child links below the page
    children = family.get_children(page)
    child_links = [utils.get_page_link(page) for page in children]
    tree = insert_subtree(subtree=child_links, tree=tree, index=page_idx)

    # Only worry about parents if it's not the root page
    if page != common.ROOT_PAGE:

        parent = family.get_parent(page)

        if parent == common.ROOT_PAGE:
            # Insert the working tree below the root page
            parent_links = [utils.get_page_link(common.ROOT_PAGE)]
            parent_idx = 0
        else:
            # Insert the working tree below the parent page in the list of parents
            parents = family.get_siblings(parent)
            parent_links = [utils.get_page_link(page) for page in parents]
            parent_idx = parents.index(parent)
        tree = insert_subtree(subtree=tree, tree=parent_links, index=parent_idx)
    return common.MD_NEWLINE.join(tree)


def insert_subtree(subtree: list[str], tree: list[str], index: int) -> list[str]:
    """Insert a subtree into a tree after the specified index."""

    index += 1  # To insert *after* the specified index.
    subtree = [MD_TAB + str(line) for line in subtree]
    tree = tree[:index] + subtree + tree[index:]
    return tree


def get_toc(page: Path) -> str:
    """Get the table of contents for a page. List only the most significant headings."""

    toc_list: list[str] = []
    page_url = utils.get_page_url(page)

    with open(page) as file:
        content = file.read()
        md = Markdown(extensions=["toc"])
        md.convert(content)

    for token in md.toc_tokens:  # type: ignore  # pylint: disable=no-member
        token_id = token["id"]
        name = token["name"]
        link = utils.get_md_link(name, f"{page_url}#{token_id}")
        toc_list.append(link)

    return common.MD_NEWLINE.join(toc_list)


def get_relative_nav(page: Path) -> str:
    """Get the parent, previous, and next Markdown links."""

    nav_head = ("Next: ", "Prev: ", "Up: ")

    (next_page, prev_page, parent) = get_nearest(page)
    relative_nav: list[str] = []

    # Get next link for any page except the last page in the entire wiki
    if next_page == common.ROOT_PAGE:
        next_link = None
    else:
        next_link = utils.get_page_link(next_page)
        relative_nav.append(nav_head[0] + next_link)

    # Get previous link for any page except the home page
    if page == common.ROOT_PAGE:
        prev_link = None
    else:
        prev_link = utils.get_page_link(prev_page)
        relative_nav.append(nav_head[1] + prev_link)

    # Get parent link for any page except for Home, or the first page in a section
    if page == common.ROOT_PAGE or prev_page == parent:
        parent_link = None
    else:
        parent_link = utils.get_page_link(parent)
        relative_nav.append(nav_head[2] + parent_link)

    return MD_TAB.join(relative_nav)


# * -------------------------------------------------------------------------------- * #
# * GET NEAREST


def get_nearest(page: Path) -> tuple[Path, Path, Path]:
    """Get the pages nearest to a page."""

    siblings = family.get_siblings(page)
    if page == common.ROOT_PAGE:
        next_page = siblings[0] if siblings else common.ROOT_PAGE
        prev_page = common.ROOT_PAGE
    else:
        page_position = siblings.index(page)
        next_page = utils.get_next(page, siblings, page_position)
        prev_page = utils.get_prev(page, siblings, page_position)

    parent = family.get_parent(page)
    return next_page, prev_page, parent
