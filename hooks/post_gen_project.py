#!/usr/bin/env python
import os
import shutil
import sys
from typing import Dict

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def remove_path(path):
    path = path.strip()
    if path and os.path.exists(path):
        # if directory else file
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(os.path.join(PROJECT_DIRECTORY, path))


def create_option_text(options: Dict):
    """
    Creates a text block from a dictionary in the format of:
    '''
    {key_0} - {value_0}
    {key_1} - {value_1}
    ...
    {key_n} - {value_n}
    Choose from {key_0, key_1, ..., key_n}:
    '''
    Args:
        options: Dictionary as options.

    Returns:

    """
    string_options = ''
    for key, value in options.items():
        string_options = f"{string_options}{key} - {value}\n"

    final_line = f"Choose from {str(list(map(int, options.keys()))).strip('[').strip(']')}: "
    string_out = string_options + final_line
    return string_out


def prompt_with_options(prompt: str,
                        return_options: Dict):
    """
    Generates a user input request based from a prompt and dictionary of return options.
    The function will ask the user for a numerical selection of one of the dictionary keys based
    on order. The value of the dictionary will be returned.

    Args:
        prompt: Question to ask the user
        return_options: Dictionary with {option name: return value} as key-value pairs.

    Returns:
    Selected value from dictionary.
    """
    # Create text prompt
    d_options = {str(i+1): s for i, s in enumerate(return_options.keys())}
    option_prompt = create_option_text(d_options)
    full_prompt = f"{prompt}\n{option_prompt}"

    # Ask for input
    user_input = input(full_prompt)
    if user_input in d_options:
        return_values = return_options[d_options[user_input]]
        return return_values
    else:
        return prompt_with_options(prompt, return_options)


if __name__ == '__main__':

    if 'experimentalist' in '{{ cookiecutter.autora_contribution_type|lower }}':
        # Base files to remove
        list_remove = ['src/autora/experiment_runner',
                       'src/autora/synthetic_data',
                       'src/autora/theorist',
                       'tests/test_theorist_example.py',
                       ]
        # Additional files to remove based on user options
        prompt = 'What type of experimentalist?'
        options = {'pooler': ['src/autora/experimentalist/sampler',
                              'tests/test_experimentalist_sampler_example.py',
                              ],
                   'sampler': ['src/autora/experimentalist/pooler',
                               'tests/test_experimentalist_pooler_example.py',
                               ]
                   }
        # Prompt user for option and extend removal list
        list_remove.extend(
            prompt_with_options(prompt=prompt,
                                return_options=options)
        )

    elif 'experiment_runner' in '{{ cookiecutter.autora_contribution_type|lower }}':
        # Base files to remove
        list_remove = ['src/autora/experimentalist',
                       'src/autora/theorist',
                       'tests/test_experimentalist_pooler_example.py',
                       'tests/test_experimentalist_sampler_example.py',
                       'tests/test_theorist_example.py',
                       ]
        # Additional files to remove based on user options
        prompt = 'What component of the experiment runner?'
        options = {
            'base experiment runner': [
                'src/autora/experiment_runner/recruitment_manager',
                'src/autora/experiment_runner/experimentation_manager',
            ],
            'experimentation manager': [
                'src/autora/experiment_runner/{{ cookiecutter.__python_name }}',
                'src/autora/experiment_runner/recruitment_manager',
            ],
            'recruitment manager': [
                'src/autora/experiment_runner/{{ cookiecutter.__python_name }}',
                'src/autora/experiment_runner/experimentation_manager',
            ],
        }
        # Prompt user for option and extend removal list
        list_remove.extend(
            prompt_with_options(prompt=prompt,
                                return_options=options)
        )

    elif 'theorist' in '{{ cookiecutter.autora_contribution_type|lower }}':
        list_remove = ['src/autora/experimentalist',
                       'src/autora/experiment_runner',
                       'tests/test_experimentalist_pooler_example.py',
                       'tests/test_experimentalist_sampler_example.py',
                       ]

    elif 'synthetic_data' in '{{ cookiecutter.autora_contribution_type|lower }}':
        list_remove = ['src/autora/experiment_runner',
                       'src/autora/experimentalist',
                       'src/autora/theorist',
                       'tests/test_experimentalist_pooler_example.py',
                       'tests/test_experimentalist_sampler_example.py',
                       'tests/test_theorist_example.py',
                       ]

    for path_remove in list_remove:
        try:
            remove_path(path_remove)
        except OSError as e:
            print(f"Error: {path_remove} : {e.strerror}")
            sys.exit(1)


