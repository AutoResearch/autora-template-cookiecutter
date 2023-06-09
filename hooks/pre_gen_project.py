import re
import sys


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

module_name = '{{ cookiecutter.__contrib_name_modulename}}'

if not re.match(MODULE_REGEX, module_name):
    print('ERROR: The project name (%s) is not a valid Python module name.' % module_name)

    #Exit to cancel project
    sys.exit(1)
