"""
Functions and structure derived from test found in
https://github.com/audreyfeldroy/cookiecutter-pypackage
"""
from contextlib import contextmanager
import shlex
import os
import subprocess
from cookiecutter.utils import rmtree
from pathlib import Path


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


def bake_and_return_readme(cookies, inputs):
    with bake_in_temp_dir(cookies, extra_context=inputs) as result:
        with open(result.project / 'README.md') as file:
            content = file.read()
            return content


def run_inside_dir(command, dirpath):
    """
    Run a command from inside a given directory, returning the exit status
    :param command: Command that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        return subprocess.check_call(shlex.split(command))


def check_output_inside_dir(command, dirpath):
    "Run a command from inside a given directory, returning the command output"
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))


def project_info(result):
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    project_dir = os.path.join(project_path, project_slug)
    return project_path, project_slug, project_dir


def check_construct(result):
    checks = [result.project.isdir(),
              result.exit_code == 0,
              result.exception is None]
    if all(checks):
        return True
    else:
        return False


def tree_list(root):
    l_tree = []
    for root, dirs, files in os.walk(root):
        for d in dirs:
            l_tree.append(os.path.join(root, d))
        for f in files:
            l_tree.append(os.path.join(root, f))
    return l_tree


def convert_os_paths(path_list):
    return_list = [Path(s) for s in path_list]
    return return_list


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies, extra_context={"contribution_name": "test"}) as result:
        assert check_construct(result)

        # Check naming of directory
        assert 'autora-theorist-test' == os.path.basename(result.project)

        # All top level files/directories are correct
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert 'mkdocs.yml' in found_toplevel_files
        assert not '.pre-commit-config.yaml' in found_toplevel_files
        assert 'pyproject.toml' in found_toplevel_files
        assert 'README.md' in found_toplevel_files
        assert '.gitignore' in found_toplevel_files
        assert not '.github' in found_toplevel_files
        assert 'tests' in found_toplevel_files
        assert 'docs' in found_toplevel_files
        assert 'mkdocs' in found_toplevel_files
        assert 'src' in found_toplevel_files


def test_basic_utils(cookies):
    with bake_in_temp_dir(cookies, extra_context={"contribution_name": "test",
                                                  "__contrib_utilities": "basic"}) as result:
        # Dynamic versioning is not set
        with open(result.project / 'pyproject.toml') as file:
            content = file.read()
        assert 'version = "0.1.0"' in content
        assert 'dynamic = ["version"]' not in content
        assert 'requires = ["setuptools", "setuptools_scm"]' not in content
        assert '[tool.setuptools_scm]' not in content

        # Check for files
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        # GitHub Actions Check
        assert '.github' not in found_toplevel_files
        # Pre-commit check
        assert '.pre-commit-config.yaml' not in found_toplevel_files


def test_advanced_utils(cookies):
    with bake_in_temp_dir(cookies, extra_context={"contribution_name": "test",
                                                  "__contrib_utilities": "advanced"}) as result:
        # Dynamic versioning check
        with open(result.project / 'pyproject.toml') as file:
            content = file.read()
        assert 'version = "0.1.0"' not in content
        assert 'dynamic = ["version"]' in content
        assert 'requires = ["setuptools", "setuptools_scm"]' in content
        assert '[tool.setuptools_scm]' in content

        # Check for files
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        # GitHub Actions Check
        assert '.github' in found_toplevel_files
        # Pre-commit check
        assert '.pre-commit-config.yaml' in found_toplevel_files


def test_pyproject_toml_population(cookies):
    with bake_in_temp_dir(cookies, extra_context={"contribution_name": "test",
                                                  "full_name": "John Doe",
                                                  "email": "jdoe@domain.com",
                                                  "project_short_description": "This is a test.",
                                                  "repository": "www.repository.com",
                                                  "license": 'BSD license'
                                                  }) as result:
        assert check_construct(result)
        with open(result.project / 'pyproject.toml') as file:
            content = file.read()

        assert 'name = "test"' in content
        assert 'description = "This is a test."' in content
        assert 'name = "John Doe"' in content
        assert 'email = "jdoe@domain.com"' in content
        assert 'repository = "www.repository.com"' in content
        assert 'license = { text = "BSD license" }'


def test_mkdocs_population(cookies):
    with bake_in_temp_dir(cookies, extra_context={"contribution_name": "test",
                                                  "repository": "www.repository.com",
                                                  }) as result:
        assert check_construct(result)
        with open(result.project / 'mkdocs.yml') as file:
            content = file.read()
        assert 'site_name: AutoRA test' in content
        assert "repo_url: 'www.repository.com'" in content


def test_theorist(cookies):
    with bake_in_temp_dir(cookies, extra_context={"contribution_name": "test-theorist",
                                                  "autora_contribution_type": "theorist [DEFAULT]",
                                                  }) as result:
        assert check_construct(result)

        # Check naming of directory
        assert 'autora-theorist-test-theorist' == os.path.basename(result.project)

        # Check source code tree structure
        basename = os.path.basename(result.project)
        l_tree = tree_list(result.project / 'src')
        l_tree = [Path(s.split(basename)[1]) for s in l_tree]
        assert l_tree == convert_os_paths(['/src/autora',
                                           '/src/autora/theorist',
                                           '/src/autora/theorist/test_theorist',
                                           '/src/autora/theorist/test_theorist/__init__.py'])


def test_experimentalist(cookies):
    with bake_in_temp_dir(cookies, extra_context={"contribution_name": "test-experimentalist",
                                                  "autora_contribution_type": "experimentalist",
                                                  }) as result:
        assert check_construct(result)

        assert 'autora-experimentalist-test-experimentalist' == os.path.basename(result.project)

        # Check source code tree structure
        basename = os.path.basename(result.project)
        l_tree = tree_list(result.project / 'src')
        l_tree = [Path(s.split(basename)[1]) for s in l_tree]
        assert l_tree == convert_os_paths(['/src/autora',
                                           '/src/autora/experimentalist',
                                           '/src/autora/experimentalist/test_experimentalist',
                                           '/src/autora/experimentalist/test_experimentalist/__init__.py'])


def test_runner(cookies):
    subtypes_raw = [
        "{% if cookiecutter.autora_contribution_type == 'experiment_runner' -%}experiment_runner [DEFAULT]{% else -%}N/A - Press Enter to skip{% endif -%}",
        "{% if cookiecutter.autora_contribution_type == 'experiment_runner' -%}experimentation_manager{% else -%}N/A - Press Enter to skip{% endif -%}",
        "{% if cookiecutter.autora_contribution_type == 'experiment_runner' -%}recruitment_manager{% else -%}N/A - Press Enter to skip{% endif -%}"]
    subtypes = ['experiment_runner [DEFAULT]', 'experimentation_manager', 'recruitment_manager']

    d_subtypes = {}
    for i, (subtype, raw) in enumerate(zip(subtypes, subtypes_raw)):
        d_inputs = {"contribution_name": "test_runner",
                    "autora_contribution_type": "experiment_runner",
                    "experiment_runner_type": raw
                    }

        with bake_in_temp_dir(cookies, extra_context=d_inputs) as result:
            assert check_construct(result)

            # Check source code tree structure
            basename = os.path.basename(result.project)
            l_tree = tree_list(result.project / 'src')
            l_tree = [Path(s.split(basename)[1]) for s in l_tree]

            # Add to dict
            d_subtypes[subtype] = {'basename': basename, 'tree': l_tree}

    # Check directory names
    assert d_subtypes['experiment_runner [DEFAULT]'][
               'basename'] == 'autora-experiment-runner-test-runner'
    assert d_subtypes['experimentation_manager'][
               'basename'] == 'autora-experiment-runner-experimentation-manager-test-runner'
    assert d_subtypes['recruitment_manager'][
               'basename'] == 'autora-experiment-runner-recruitment-manager-test-runner'

    # Check directory trees
    assert d_subtypes['experiment_runner [DEFAULT]']['tree'] == \
           convert_os_paths(['/src/autora',
                             '/src/autora/experiment_runner',
                             '/src/autora/experiment_runner/test_runner',
                             '/src/autora/experiment_runner/test_runner/__init__.py'])

    assert d_subtypes['experimentation_manager']['tree'] == \
           convert_os_paths(['/src/autora',
                             '/src/autora/experiment_runner',
                             '/src/autora/experiment_runner/experimentation_manager',
                             '/src/autora/experiment_runner/experimentation_manager/test_runner',
                             '/src/autora/experiment_runner/experimentation_manager/test_runner/__init__.py'])

    assert d_subtypes['recruitment_manager']['tree'] == \
           convert_os_paths(['/src/autora',
                             '/src/autora/experiment_runner',
                             '/src/autora/experiment_runner/recruitment_manager',
                             '/src/autora/experiment_runner/recruitment_manager/test_runner',
                             '/src/autora/experiment_runner/recruitment_manager/test_runner/__init__.py'])


def test_custom(cookies):
    d_inputs = {"contribution_name": "test_custom",
                "autora_contribution_type": "custom",
                "custom_autora_contribution_type": "new_type"
                }
    with bake_in_temp_dir(cookies, extra_context=d_inputs) as result:
        assert check_construct(result)

        # Check source code tree structure
        basename = os.path.basename(result.project)
        l_tree = tree_list(result.project / 'src')
        l_tree = [Path(s.split(basename)[1]) for s in l_tree]

        assert basename == 'autora-new-type-test-custom'
        assert l_tree == convert_os_paths(['/src/autora',
                                           '/src/autora/new_type',
                                           '/src/autora/new_type/test_custom',
                                           '/src/autora/new_type/test_custom/__init__.py'])


def test_readme_populate_defaults(cookies):
    d_inputs = {"contribution_name": "test_readme"}
    content = bake_and_return_readme(cookies, d_inputs)

    slug_text = f"(a sensible name for the repository would be " \
                f"autora-theorist-{d_inputs['contribution_name'].lower().replace('_', '-')})"
    assert slug_text in content

    full_path_text = "add your code to `src/autora/theorist/test_readme/__init__.py`"
    assert full_path_text in content

    python_name_text = 'test cases in `tests/test_test_readme.py`.'
    assert python_name_text in content


def test_readme_population_by_contribution_type(cookies):
    l_contribution_types = ["theorist [DEFAULT]", "experimentalist", "experiment_runner"]
    d_contribution_subtypes = {'experiment_runner': ['experiment_runner', 'experimentation_manager',
                                                     'recruitment_manager', "synthetic"]}
    d_subtypes_raw = {
        "experiment_runner": "{% if cookiecutter.autora_contribution_type == 'experiment_runner' -%}experiment_runner [DEFAULT]{% else -%}N/A - Press Enter to skip{% endif -%}",
        "experimentation_manager": "{% if cookiecutter.autora_contribution_type == 'experiment_runner' -%}experimentation_manager{% else -%}N/A - Press Enter to skip{% endif -%}",
        "recruitment_manager": "{% if cookiecutter.autora_contribution_type == 'experiment_runner' -%}recruitment_manager{% else -%}N/A - Press Enter to skip{% endif -%}",
        "synthetic": "{% if cookiecutter.autora_contribution_type == 'experiment_runner' -%}synthetic{% else -%}N/A - Press Enter to skip{% endif -%}"
    }

    # Create all permutations of readme files
    d_readme = {}
    # Loop by contribution type
    for contriubtion_type in l_contribution_types:
        d_inputs = {"contribution_name": "test_readme",
                    "autora_contribution_type": contriubtion_type}
        # If no subtypes
        if contriubtion_type not in d_contribution_subtypes:
            # Generate project and return readme contents
            d_readme[contriubtion_type] = bake_and_return_readme(cookies, d_inputs)

        # If subtypes
        elif contriubtion_type in d_contribution_subtypes:
            for subtype in d_contribution_subtypes[contriubtion_type]:
                if contriubtion_type == 'experiment_runner':
                    d_inputs["experiment_runner_type"] = d_subtypes_raw[subtype]
                # Generate project and return readme contents
                d_readme[f"{contriubtion_type}-{subtype}"] = \
                    bake_and_return_readme(cookies, d_inputs)

    # Assert presence and absence of appropriate headers
    ## Theorist
    theorist_absent = ["### Experimentalist", "### Experiment Runners"]
    assert '### Theorist' in d_readme['theorist [DEFAULT]'] and \
           all([s not in d_readme['theorist [DEFAULT]'] for s in theorist_absent])

    ## Experimentalist
    experimentalist_absent = ["### Theorist", "### Experiment Runners"]
    assert '### Experimentalist' in d_readme['experimentalist'] and \
           all([s not in d_readme['experimentalist'] for s in experimentalist_absent])

    ## Experiment Runner
    ### Base Runner
    er_absent = ["### Theorist", "### Experimentalist"]
    assert '### Experiment Runners' in d_readme['experiment_runner-experiment_runner'] and \
           all([s not in d_readme['experiment_runner-experiment_runner'] for s in er_absent])
    assert '*Recruitment Manager*' not in d_readme['experiment_runner-experiment_runner']
    assert '*Experimentation Manager*' not in d_readme['experiment_runner-experiment_runner']
    ### Experimentation manager
    assert '*Experimentation Manager*' in d_readme['experiment_runner-experimentation_manager']
    assert '*Recruitment Manager*' not in d_readme['experiment_runner-experimentation_manager']
    ### Recruitment manager
    assert '*Recruitment Manager*' in d_readme['experiment_runner-recruitment_manager']
    assert '*Experimentation Manager*' not in d_readme['experiment_runner-recruitment_manager']
    ### Synthetic Data
    assert '*Synthetic*' in d_readme['experiment_runner-synthetic']


def test_readme_population_by_options(cookies):
    content_gh = bake_and_return_readme(cookies,
                                        {"contribution_name": "test_readme",
                                         "__contrib_utilities": "advanced"})
    assert '#### Step 5.2 Publish via GitHub Actions' in content_gh
    assert '#### Step 5.2: Publish via Twine' not in content_gh

    content_twine_no_dv = bake_and_return_readme(cookies,
                                                 {"contribution_name": "test_readme",
                                                  "__contrib_utilities": "basic",
                                                  }
                                                 )
    assert '#### Step 5.2: Publish via Twine' in content_twine_no_dv
    assert '#### Dynamic versioning' not in content_twine_no_dv
    assert '- version' in content_twine_no_dv
