from pathlib import Path

# Patterns specific to GitHub Wiki
PAGE_PATTERN = "[!_]*.md"
SIDEBAR_FILENAME = "_Sidebar.md"
FOOTER_FILENAME = "_Footer.md"

# The origin repo should be a GitHub wiki, and pages should be in the "wiki" subfolder
ROOT_NAME = "wiki"

# Get pages to be used throughout the module
WIKI_ROOT = Path(ROOT_NAME)

if not WIKI_ROOT.exists():
    WIKI_ROOT.mkdir()
    (WIKI_ROOT / "Home.md").touch()

PAGES = sorted(WIKI_ROOT.glob(f"**/{PAGE_PATTERN}"))
ROOT_PAGE = PAGES[-1]

# Two newlines signifies a paragraph break in Markdown.
MD_NEWLINE = "  \n"
