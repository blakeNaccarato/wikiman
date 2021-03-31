import pytest
import patchy


@pytest.fixture(scope="session", autouse=True)
def patchy_root():
    pass
