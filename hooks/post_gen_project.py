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
                       'src/autora/experiment_runner',
                       'tests/test_theorist_example.py',
                       ]
        answer = input("What type of experimentalist?")

        valid = False
        while not valid:
            print(f'Input: {answer}')
            if answer == 'pooler':
                list_remove.extend(['src/autora/experimentalist/sampler',
                                    'tests/test_experimentalist_sampler_example.py',
                                    ])
                valid = True
            elif answer == 'sampler':
                list_remove.extend(['src/autora/experimentalist/pooler',
                                    'tests/test_experimentalist_pooler_example.py',
                                    ])
                valid = True
            else:
                print(f"Invalid option. Choose from [pooler, sampler]")
                answer = input("What type of experimentalist?")

    if 'theorist' in '{{ cookiecutter.autora_contribution_type|lower }}':
        list_remove = ['src/autora/experimentalist',
                       'src/autora/experiment_runner',
                       'tests/test_experimentalist_pooler_example.py',
                       'tests/test_experimentalist_sampler_example.py',
                       ]

    if 'experiment_runner' in '{{ cookiecutter.autora_contribution_type|lower }}':
        list_remove = ['src/autora/experimentalist',
                       'src/autora/theorist',
                       'tests/test_experimentalist_pooler_example.py',
                       'tests/test_experimentalist_sampler_example.py',
                       'tests/test_theorist_example.py',
                       ]

    if '{{ cookiecutter.use_github_actions }}' == 'no':
        list_remove.extend(['.github'])

    for path_remove in list_remove:
        try:
            remove_path(path_remove)
        except OSError as e:
            print(f"Error: {path_remove} : {e.strerror}")
            sys.exit(1)


