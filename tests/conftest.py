from dataclasses import dataclass
from pathlib import Path

import pytest
from wikiman import git


@pytest.fixture(autouse=True)
def patch(monkeypatch):
    @dataclass
    class Url:
        url = "https://github.com/blakeNaccarato/wikiman/wikiman.wiki.git"

    @dataclass
    class Remotes:
        origin = Url()

    monkeypatch.setattr(git.Repo, "remotes", Remotes)
