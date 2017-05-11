import pytest

from rbu.pull_request import (setup_repo_for_pr,
                              commits_diff_between_branches)
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


@pytest.mark.setup_repo
def test_commits_diff_between_branches(setup_repo):
    commits = commits_diff_between_branches('master', '_rbu_pr_branch', setup_repo)
    assert len(commits) == 2
    assert '404ddb8' in commits and commits['404ddb8'] == 'Changes nothing'
    assert 'aa3edfe' in commits and commits['aa3edfe'] == 'Improves performance'
