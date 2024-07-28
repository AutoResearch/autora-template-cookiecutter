import re
import sys
import os


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

module_name = '{{ cookiecutter.__contrib_name_modulename}}'

is_current_directory = '{{ cookiecutter.use_current_directory }}'
parent_dir = os.path.basename(os.path.realpath(os.path.curdir))
slug = '{{ cookiecutter.__project_slug }}'


if not re.match(MODULE_REGEX, module_name):
    print('ERROR: The project name (%s) is not a valid Python module name.' % module_name)

    #Exit to cancel project
    sys.exit(1)

if is_current_directory == 'yes':
    if parent_dir != slug:
        print(f'ERROR: When using `use_current_directory`, '
              f'the parent directory `{parent_dir} '
              f'must match the contribution name `{slug}`')
        sys.exit(1)


