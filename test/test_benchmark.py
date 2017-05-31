import tempfile
import glob
from os.path import join, dirname

import pytest

from rbu.benchmark import benchmark_commits, compare_benchmarks
from test.consts import COMMITS, ERRORED_COMMIT


@pytest.mark.setup_repo
def test_benchmark_commits(setup_repo):
    with tempfile.TemporaryDirectory() as directory:
        benchmark_commits(COMMITS, setup_repo, directory)

        result = set(glob.glob(join(directory, '*.txt')))
        expected = {join(directory, sha + '.txt') for sha in COMMITS}

        with open(join(directory, ERRORED_COMMIT + '.txt')) as f:
            assert f.readline() == 'ERROR RUNNING BENCHMARK'
        assert result == expected


def test_compare_benchmarks():
    assets_dir = join(dirname(__file__), 'assets', 'benchmark_outputs')
    comparisons = compare_benchmarks('24ec188', COMMITS.keys(), assets_dir)

    assert comparisons['1f4db65'] != 'no significant variations'
    assert comparisons['21a29f0'] == 'no significant variations'
    assert comparisons[ERRORED_COMMIT] == 'can not compared because benchmarking failed'
