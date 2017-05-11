import tempfile
import glob
from os.path import join, dirname

import pytest

from rbu.benchmark import benchmark_commits, compare_benchmarks

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


def test_compare_benchmarks():
    assets_dir = join(dirname(__file__), 'assets', 'benchmark_outputs')
    comparisons = compare_benchmarks('24ec188', ['404ddb8', 'aa3edfe'], assets_dir)

    assert comparisons['aa3edfe'] != 'no significant variations'
    assert comparisons['404ddb8'] == 'no significant variations'
