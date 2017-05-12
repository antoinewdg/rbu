import os
import subprocess


def check_for_cargo_benchcmp():
    try:
        subprocess.check_output('cargo benchcmp --help', shell=True)
    except subprocess.CalledProcessError as e:
        raise Exception("cargo-benchcmp is not installed, please install with "
                        "`cargo install cargo-benchcmp`")


def check_environment_variable(name, msg_end=''):
    if name not in os.environ:
        msg = 'The environment variable {} must be set {}'.format(name, msg_end)
        raise Exception(msg)


def check_github_api_env_vars():
    check_environment_variable('RBU_GH_USERNAME', 'to access Github API')
    check_environment_variable('RBU_GH_TOKEN', 'to access Github API')
