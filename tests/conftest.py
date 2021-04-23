import shutil
from pathlib import Path

import pytest

WIKI_ROOT_NAME = "wiki"

WIKI_ROOT = Path("wiki")
if not WIKI_ROOT.exists():
    WIKI_ROOT.mkdir()

TESTS_ROOT = Path("tests")
TESTS_WIKI_ROOT = TESTS_ROOT / WIKI_ROOT_NAME


# * -------------------------------------------------------------------------------- * #
# * MAIN


def main():
    """Restore the wiki after importing conftest but before ever importing wikiman."""

    restore_wiki()


# * -------------------------------------------------------------------------------- * #
# * GLOBAL AUTOMATIC CONTEXTS


@pytest.fixture(scope="session", autouse=True)
def REMOVE_WIKI_AFTER_ALL_TESTS():
    """Remove the wiki directory at the end of the testing session."""

    yield
    shutil.rmtree(WIKI_ROOT)


# * -------------------------------------------------------------------------------- * #
# * CONTEXTS


@pytest.fixture()
def RESTORE_WIKI():
    """Restore the wiki directory before and after running a test."""

    restore_wiki()
    yield
    restore_wiki()


# * -------------------------------------------------------------------------------- * #
# * RESOURCES


@pytest.fixture()
def EXPECTED_WIKI(request, RESTORE_WIKI) -> Path:
    """Get the expected final state of the wiki.

    Search the "tests" folder for "wiki" subfolders to folders matching the test module
    name (e.g. "test_wikiman"), the test itself (e.g. "test_create_page"), or the
    `test_id` of the parametrized test (if parametrized at all, e.g. "dashes").

    For example:

      tests
      │
      │ conftest.py
      │ test_wikiman.py
      │
      └───test_wikiman
          │
          ├───test_create_page
          │   │
          │   ├───dashes
          │   │   │
          │   │   └───wiki  # 1st priority, if it exists.
          │   │
          │   └───wiki  # 2nd priority, if it exists.
          │
          └───wiki  # 3rd priority, if it exists. Exception if none exist.
    """

    is_parametrized = any(
        (marker.name == "parametrize" for marker in request.node.iter_markers())
    )

    module = request.node.module
    test_name = request.node.originalname

    # Get module-, test-, and parametrized-level paths
    module_wiki = TESTS_ROOT / module.__name__ / WIKI_ROOT_NAME
    test_wiki = module_wiki.parent / test_name / WIKI_ROOT_NAME
    if is_parametrized:
        test_id = request.node.name.split("[")[1].split("-")[0]
        parametrized_wiki = test_wiki.parent / test_id / WIKI_ROOT_NAME
    else:
        parametrized_wiki = None

    # Look in parametrized-, then test-, then module-level paths for an expected wiki
    if is_parametrized and parametrized_wiki.exists():
        wiki = parametrized_wiki
    if test_wiki.exists():
        wiki = test_wiki
    elif module_wiki.exists():
        wiki = module_wiki
    else:
        raise pytest.UsageError("No wiki found for expected results to this test.")

    return wiki


# * -------------------------------------------------------------------------------- * #
# * UTILITY FUNCTIONS


def restore_wiki():
    """Restore the wiki directory."""

    shutil.rmtree(WIKI_ROOT)
    shutil.copytree(TESTS_WIKI_ROOT, WIKI_ROOT)


# * -------------------------------------------------------------------------------- * #
# * RUN MAIN

main()
