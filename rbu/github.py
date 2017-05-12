import re
from os import environ, getcwd

import requests
from git import Repo

from rbu.pull_request import (setup_repo_for_pr,
                              commits_diff_between_branches,
                              head_commit,
                              generate_pr_comment)

from rbu.benchmark import (benchmark_commits,
                           compare_benchmarks)


def request_github_api(endpoint, remote_url, data=None):
    org, repo_name = remote_url.split('/')[-2:]
    repo_name = repo_name.rpartition('.')[0]
    url = 'https://api.github.com/repos/{}/{}{}'.format(
        org, repo_name, endpoint
    )

    username = environ['RBU_GH_USERNAME']
    token = environ['RBU_GH_TOKEN']

    if data is None:
        r = requests.get(url, auth=(username, token))
    else:
        r = requests.post(url, auth=(username, token), json=data)

    return r.json()


def post_pr_comment(pr_id, remote_url, comment):
    data = {'body': comment}
    request_github_api('/issues/{}/comments'.format(pr_id), remote_url, data)


def benchmark_github_pr(pr_id, remote_url, benchmarks_dir):
    repo = Repo(getcwd())
    with setup_repo_for_pr(pr_id, repo, remote_url):
        commits = commits_diff_between_branches('_rbu_upstream/master', '_rbu_pr_branch', repo)
        master_sha, master_title = head_commit(repo, '_rbu_upstream/master')
        benchmark_commits({**commits, master_sha: master_title}, repo, benchmarks_dir)
        compare_benchmarks(master_sha, commits, benchmarks_dir)
        comment = generate_pr_comment((master_sha, master_title), commits, benchmarks_dir)
        post_pr_comment(pr_id, remote_url, comment)
