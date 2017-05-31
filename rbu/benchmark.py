import subprocess


def _run_warmup(repo, base_sha):
    print('  - warming up...')
    repo.git.checkout(base_sha)
    for _ in range(3):
        subprocess.check_output('cargo bench', shell=True)


def benchmark_commits(commits, repo, output_dir, warmup=True):
    successful_shas = []
    print('Running benchmarks:')
    if warmup:
        _run_warmup(repo, next(iter(commits.items()))[0])

    for sha, title in commits.items():
        print(' - benchmarking commit {}: {}'.format(sha, title))
        repo.git.checkout(sha)
        filename = '{}/{}.txt'.format(output_dir, sha)
        cmd = 'cargo bench > {}'.format(filename)
        try:
            subprocess.check_output(cmd, shell=True)
            successful_shas.append(sha)
        except subprocess.CalledProcessError:
            with open(filename, 'w') as file:
                file.write('ERROR RUNNING BENCHMARK')

    return successful_shas


def _has_commit_been_benchmarked(sha, benchmark_dir):
    with open('{}/{}.txt'.format(benchmark_dir, sha)) as f:
        try:
            if next(f) == 'ERROR RUNNING BENCHMARK':
                return False
        except StopIteration:
            return False
    return True


def compare_benchmarks(base_sha, others_sha, benchmark_dir):
    comparisons = {}
    if not _has_commit_been_benchmarked(base_sha, benchmark_dir):
        return comparisons

    for sha in others_sha:
        if not _has_commit_been_benchmarked(sha, benchmark_dir):
            comparisons[sha] = 'can not compared because benchmarking failed'
            continue
        cmd = 'cargo benchcmp {dir}/{sha_1}.txt {dir}/{sha_2}.txt --threshold 2 --variance' \
            .format(dir=benchmark_dir, sha_1=base_sha, sha_2=sha)
        out = subprocess.check_output(cmd, shell=True).decode('utf-8')
        if out == '':
            out = 'no significant variations'
        comparisons[sha] = out

    return comparisons
