from collections import OrderedDict

TEST_REPO_NAME = 'rbu-test-repo'
TEST_REPO_URL = 'https://github.com/antoinewdg/rbu-test-repo.git'

COMMITS = OrderedDict({
    '1f4db65': 'Improves performance',
    '21a29f0': 'Does not change anything',
    'b201bbf': 'Does not compile',
})

ERRORED_COMMIT = 'b201bbf'
