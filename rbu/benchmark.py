import subprocess


def _run_warmup():
    print('  - warming up...')
    for _ in range(3):
        subprocess.check_output('cargo bench', shell=True)


def benchmark_commits(commits, repo, output_dir, warmup=True):
    print('Running benchmarks:')
    if warmup:
        _run_warmup()

    for sha, title in commits.items():
        print(' - benchmarking commit {}: {}'.format(sha, title))
        repo.git.checkout(sha)
        cmd = 'cargo bench > {}/{}.txt'.format(output_dir, sha)
        subprocess.check_output(cmd, shell=True)
