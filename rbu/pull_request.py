from collections import OrderedDict
from contextlib import contextmanager

import cpuinfo

from rbu.benchmark import compare_benchmarks


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

    try:
        yield
    finally:
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


def head_commit(repo, branch):
    out = repo.git.log('--oneline', '-n', '1', branch)
    sha, _, title = out.partition(' ')
    return sha, title


_INDIVIDUAL_BENCH_TEMPLATE = """
<details><summary>{sha} {title}</summary>
  <p>\n\n
\n\n
```bash\n
{body}\n\n
```\n\n

</p></details>
"""

_COMPARISON_TEMPLATE = """
<details><summary>{sha} {title}</summary>
  <p>\n\n
\n\n
```bash\n
{body}\n\n
```\n\n

</p></details>
"""


def generate_pr_comment(master_commit, commits, benchmarks_dir):
    # Comparison benchmarks
    master_sha, master_title = master_commit
    comment = '## Comparing to master ({})\nusing `--threshold 2, latest commit first`'.format(master_sha)

    comparisons = compare_benchmarks(master_sha, commits, benchmarks_dir)
    for sha, title in commits.items():
        compare = comparisons[sha]
        comment += _COMPARISON_TEMPLATE.format(sha=sha, title=title, body=compare)

    # Individual benchmarks
    comment += '\n## Individual benchmarks\n'

    for k, (sha, title) in enumerate(list(commits.items()) + [master_commit]):
        with open('{}/{}.txt'.format(benchmarks_dir, sha)) as f:
            bench = f.read()
        comment += _INDIVIDUAL_BENCH_TEMPLATE.format(sha=sha, title=title, body=bench)

    info = cpuinfo.get_cpu_info()
    if info is not None:
        comment += '\n<br>**CPU**: {}'.format(info['brand'])

    return comment
