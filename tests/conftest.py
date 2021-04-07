"""Test configuration."""

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


@pytest.fixture(autouse=True)
def restore_wiki_before_test():
    """Restore the wiki directory before running a test."""

    shutil.rmtree(wm.WIKI_ROOT)
    shutil.copytree(WIKI_ROOT, wm.WIKI_ROOT)


# * -------------------------------------------------------------------------------- * #
# * RESOURCES


@pytest.fixture()
def expected_wiki(request) -> Path:
    """Get the expected final state of the wiki."""

    is_parametrized = any(
        (marker.name == "parametrize" for marker in request.node.iter_markers())
    )

    module = request.node.module
    test_name = request.node.originalname
    root = Path(module.__file__).parent

    module_wiki = root / module.__name__ / WIKI_ROOT_NAME
    test_wiki = module_wiki.parent / test_name / WIKI_ROOT_NAME
    if is_parametrized:
        test_id = request.node.name.split("[")[1].split("-")[0]
        parametrized_wiki = test_wiki.parent / test_id / WIKI_ROOT_NAME

    if is_parametrized and parametrized_wiki.exists():
        wiki = parametrized_wiki
    if test_wiki.exists():
        wiki = test_wiki
    elif module_wiki.exists():
        wiki = module_wiki
    else:
        raise pytest.UsageError("No wiki found for expected results to this test.")

    return wiki
