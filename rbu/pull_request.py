import os
from contextlib import contextmanager

from git import Repo


@contextmanager
def setup_repo_for_pr(pr_id, repo, remote_url):
    """
    Sets up correct remote and branch for 
    a PR.
    :param pr_id: 
    :param repo: 
    :param remote_url: 
    :return: 
    """
    repo.git.remote('add', '_rbu_upstream', remote_url)
    repo.git.fetch('_rbu_upstream', 'master')
    repo.git.fetch('_rbu_upstream',
                   'pull/{}/head:_rbu_pr_branch'.format(pr_id))

    yield

    repo.git.branch('-D', '_rbu_pr_branch')
    repo.git.remote('remove', '_rbu_upstream')
