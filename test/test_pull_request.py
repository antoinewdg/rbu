import pytest

from rbu.pull_request import (setup_repo_for_pr,
                              commits_diff_between_branches,
                              head_commit)
from test.consts import TEST_REPO_URL, COMMITS


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


@pytest.mark.repo
def test_setup_pr_repo_with_exceptions(repo):
    class FakeException(Exception):
        pass

    try:
        with setup_repo_for_pr(1, repo, TEST_REPO_URL):
            names = {h.name for h in repo.heads}
            assert '_rbu_pr_branch' in names
            assert TEST_REPO_URL in repo.remotes['_rbu_upstream'].urls
            raise FakeException('')
    except FakeException:
        names = {h.name for h in repo.heads}
        assert '_rbu_pr_branch' not in names
        names = {r.name for r in repo.remotes}
        assert '_rbu_upstream' not in names


@pytest.mark.setup_repo
def test_commits_diff_between_branches(setup_repo):
    commits = commits_diff_between_branches('master', '_rbu_pr_branch', setup_repo)
    assert commits == COMMITS


@pytest.mark.setup_repo
def test_head_commit(setup_repo):
    sha, title = head_commit(setup_repo, '_rbu_pr_branch')
    assert sha == '1f4db65'
    assert title == 'Improves performance'
