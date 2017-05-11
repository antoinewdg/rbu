import tempfile
import glob
from os.path import join

import pytest

from rbu.benchmark import benchmark_commits

COMMITS = {
    '404ddb8': 'Changes nothing',
    'aa3edfe': 'Improves performance'
}


@pytest.mark.setup_repo
def test_benchmark_commits(setup_repo):
    with tempfile.TemporaryDirectory() as directory:
        benchmark_commits(COMMITS, setup_repo, directory)

        result = glob.glob(join(directory, '*.txt'))
        for sha in COMMITS:
            assert join(directory, sha + '.txt') in result
