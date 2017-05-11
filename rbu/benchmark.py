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


def compare_benchmarks(base_sha, others_sha, benchmark_dir):
    comparisons = {}
    for sha in others_sha:
        cmd = 'cargo benchcmp {dir}/{sha_1}.txt {dir}/{sha_2}.txt --threshold 2 --variance' \
            .format(dir=benchmark_dir, sha_1=base_sha, sha_2=sha)
        out = subprocess.check_output(cmd, shell=True).decode('utf-8')
        if out == '':
            out = 'no significant variations'
        comparisons[sha] = out

    return comparisons
