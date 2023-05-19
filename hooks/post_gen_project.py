#!/usr/bin/env python
import os
import shutil

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
    if 'not_applicable' == '{{ cookiecutter.__contrib_subtype }}':
        shutil.move(
            'src/autora/{{ cookiecutter.__contrib_type_modulename }}/not_applicable/{{ cookiecutter.__contrib_name_modulename }}',
            'src/autora/{{ cookiecutter.__contrib_type_modulename }}/{{ cookiecutter.__contrib_name_modulename }}',)
        os.rmdir('src/autora/{{ cookiecutter.__contrib_type_modulename }}/not_applicable')
    # Remove .pre-commit-config.yaml file if not using pre-commit hooks
    if 'basic' == '{{ cookiecutter.__contrib_utilities }}':
        os.remove('.pre-commit-config.yaml')
    # Remove .github directory if not using github actions
    if 'basic' == '{{ cookiecutter.__contrib_utilities }}':
        shutil.rmtree('.github')





