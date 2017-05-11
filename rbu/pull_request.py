from collections import OrderedDict
from contextlib import contextmanager


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


def commits_diff_between_branches(base, divergent, repo):
    """
    Get the commits in branch `divergent` that are not in `base`.
    
    :param base: 
    :param divergent: 
    :param repo: 
    :return: an `OrderedDict whose keys are the sha1 of the commits
            and values the commit titles
    """
    commits = OrderedDict()
    out = repo.git.log('--oneline', '{}..{}'.format(base, divergent))
    for line in out.split('\n'):
        sha, _, title = line.partition(' ')
        commits[sha] = title

    return commits
