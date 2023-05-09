#!/usr/bin/env python
import os
import shutil
import sys

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_path(path):
    path = path.strip()
    if path and os.path.exists(path):
        # if directory else file
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(os.path.join(PROJECT_DIRECTORY, path))


if __name__ == '__main__':

    if 'experimentalist' in '{{ cookiecutter.autora_contribution_type|lower }}':
        list_remove = ['src/autora/theorist',
                       'tests/test_theorist_example.py',
                       ]

    if 'theorist' in '{{ cookiecutter.autora_contribution_type|lower }}':
        list_remove = ['src/autora/experimentalist',
                       'tests/test_experimentalist_pooler_example.py',
                       'tests/test_experimentalist_sampler_example.py',
                       ]

    for path_remove in list_remove:
        try:
            remove_path(path_remove)
        except OSError as e:
            print(f"Error: {path_remove} : {e.strerror}")
            sys.exit(1)


