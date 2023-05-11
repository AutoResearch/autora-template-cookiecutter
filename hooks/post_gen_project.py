#!/usr/bin/env python
import os
import shutil
import sys
from typing import Dict

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

def move_files_to_parent_folder(folder_path):
    parent_folder = os.path.dirname(folder_path)

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path):
            shutil.move(file_path, parent_folder)
        elif os.path.isdir(file_path):
            move_files_to_parent_folder(file_path)

    if not os.listdir(folder_path):
        os.rmdir(folder_path)

if __name__ == '__main__':
    # Move file to upper level if no contribution subtype
    if 'not_applicable' == '{{ cookiecutter.__contribution_subtype }}':
        shutil.move(
            'src/autora/{{ cookiecutter.__autora_contribution_type }}/not_applicable/{{ cookiecutter.__python_name }}',
            'src/autora/{{ cookiecutter.__autora_contribution_type }}/{{ cookiecutter.__python_name }}',)
        os.rmdir('src/autora/{{ cookiecutter.__autora_contribution_type }}/not_applicable')
    # Remove .pre-commit-config.yaml file if no github-actions
    if 'no' == '{{ cookiecutter.use_pre_commit_hooks }}':
        os.remove('.pre-commit-config.yaml')




