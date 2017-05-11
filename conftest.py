import os

import pytest
from git import Repo, Git

from test.consts import TEST_REPO_NAME, TEST_REPO_URL


@pytest.fixture()
def repo():
    if not os.path.isdir('test_repo'):
        Git().clone(TEST_REPO_URL, 'test_repo')
    return Repo('test_repo')
