import pytest

from rbu.pull_request import setup_repo_for_pr
from test.consts import TEST_REPO_URL


@pytest.mark.repo
def test_setup_pr_repo(repo):
    with setup_repo_for_pr(1, repo, TEST_REPO_URL):
        names = {h.name for h in repo.heads}
        assert '_rbu_pr_branch' in names
        assert TEST_REPO_URL in repo.remotes['_rbu_upstream'].urls

    names = {h.name for h in repo.heads}
    assert '_rbu_pr_branch' not in names
    names = {r.name for r in repo.remotes}
    assert '_rbu_upstream' not in names
