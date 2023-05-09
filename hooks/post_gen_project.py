#!/usr/bin/env python
import os
import shutil
import sys

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(dir_path):
    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))


if __name__ == '__main__':

    if 'experimentalist' in '{{ cookiecutter.autora_contribution_type|lower }}':
        remove_dir('src/autora/theorist')
        remove_file('tests/test_theorist_example.py')

    if 'theorist' in '{{ cookiecutter.autora_contribution_type|lower }}':
        remove_dir('src/autora/experimentalist')
        remove_file('tests/test_experimentalist_pooler_example.py')
        remove_file('tests/test_experimentalist_sampler_example.py')

