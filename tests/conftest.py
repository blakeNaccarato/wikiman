# pylint: disable=missing-module-docstring, redefined-outer-name, unused-argument, wrong-import-order

import shutil
from pathlib import Path

import pytest
import wikiman as wm

WIKI_ROOT_NAME = "wiki"
TESTS_ROOT = Path("tests")
WIKI_ROOT = TESTS_ROOT / WIKI_ROOT_NAME


# * -------------------------------------------------------------------------------- * #
# * AUTOUSE FIXTURES


@pytest.fixture(scope="session", autouse=True)
def remove_wiki_after_all_tests():
    """Remove the wiki directory at the end of the testing session."""

    yield
    shutil.rmtree(wm.WIKI_ROOT)


# * -------------------------------------------------------------------------------- * #
# * RESOURCES


@pytest.fixture()
def expected_wiki(request, restore_wiki_before_test) -> Path:
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


@pytest.fixture()
def restore_wiki_before_test():
    """Restore the wiki directory before running a test."""

    shutil.rmtree(wm.WIKI_ROOT)
    shutil.copytree(WIKI_ROOT, wm.WIKI_ROOT)
