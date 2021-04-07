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
def restore_wiki_after_all_tests():
    """Restore the wiki directory at the end of the testing session."""

    yield
    restore_wiki()


@pytest.fixture(autouse=True)
def restore_wiki_before_test():
    """Restore the wiki directory before running a test."""

    restore_wiki()


def restore_wiki():
    """Restore the wiki directory."""

    shutil.rmtree(wm.ROOT)
    shutil.copytree(WIKI_ROOT, wm.ROOT)


# * -------------------------------------------------------------------------------- * #
# * RESOURCES


@pytest.fixture()
def expected_wiki(request) -> Path:
    """Get the expected final state of the wiki."""

    module = request.node.module
    test_name = request.node.originalname

    root = Path(module.__file__).parent

    module_root = root / module.__name__
    module_expected_wiki = module_root / WIKI_ROOT_NAME

    test_root = module_root / test_name
    test_expected_wiki = test_root / WIKI_ROOT_NAME

    is_parametrized = any(
        (marker.name == "parametrize" for marker in request.node.iter_markers())
    )
    if is_parametrized:
        test_id = request.node.name.split("[")[1].split("-")[0]
        test_id_root = test_root / test_id
        test_id_expected_wiki = test_id_root / WIKI_ROOT_NAME

    if is_parametrized and test_id_expected_wiki.exists():
        expected_directory = test_id_expected_wiki
    if test_expected_wiki.exists():
        expected_directory = test_expected_wiki
    elif module_expected_wiki.exists():
        expected_directory = module_expected_wiki
    else:
        raise pytest.UsageError("No wiki found for expected results to this test.")

    return expected_directory
