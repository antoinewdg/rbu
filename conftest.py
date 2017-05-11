import os

import pytest
from git import Repo, Git

from rbu.pull_request import setup_repo_for_pr
from test.consts import TEST_REPO_NAME, TEST_REPO_URL


@pytest.fixture()
def repo():
    if not os.path.isdir('test_repo'):
        Git().clone(TEST_REPO_URL, 'test_repo')
    return Repo('test_repo')


@pytest.fixture()
def setup_repo():
    if not os.path.isdir('test_repo'):
        repo = Git().clone(TEST_REPO_URL, 'test_repo')
    else:
        repo = Repo('test_repo')
    os.chdir('test_repo')

    with setup_repo_for_pr(1, repo, TEST_REPO_URL):
        yield repo
