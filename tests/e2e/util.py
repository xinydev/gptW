import os
from contextlib import contextmanager
from subprocess import check_output
from typing import Generator

_dname = os.path.dirname

REPO_ROOT = _dname(_dname(_dname(os.path.abspath(__file__))))


@contextmanager
def cd(path: str) -> Generator:
    # Change directory while inside context manager
    cwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(cwd)


def run(command: str):
    return check_output(command, shell=True)
