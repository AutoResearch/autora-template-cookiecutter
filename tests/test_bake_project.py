"""
Functions and structure derived from test found in
https://github.com/audreyfeldroy/cookiecutter-pypackage
"""
from contextlib import contextmanager
import shlex
import os
import subprocess
from cookiecutter.utils import rmtree


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


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies, extra_context={"contribution_name": "test"}) as result:
        assert check_construct(result)

        # Check naming of directory
        assert 'autora-theorist-test' == os.path.basename(result.project)

        # All top level files/directories are correct
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert 'mkdocs.yml' in found_toplevel_files
        assert '.pre-commit-config.yaml' in found_toplevel_files
        assert 'pyproject.toml' in found_toplevel_files
        assert 'README.md' in found_toplevel_files
        assert '.gitignore' in found_toplevel_files
        assert '.github' in found_toplevel_files
        assert 'tests' in found_toplevel_files
        assert 'docs' in found_toplevel_files
        assert 'mkdocs' in found_toplevel_files
        assert 'src' in found_toplevel_files


def test_dynamic_numbering(cookies):
    # Test use_dynamic_versioning = yes
    with bake_in_temp_dir(cookies, extra_context={"contribution_name": "test",
                                                  "use_dynamic_versioning": "yes"}) as result:
        with open(result.project / 'pyproject.toml') as file:
            content = file.read()
        assert 'dynamic = ["version"]' in content
        assert 'version = "0.1.0"' not in content
        assert 'requires = ["setuptools", "setuptools_scm"]' in content
        assert '[tool.setuptools_scm]' in content

    # Test use_dynamic_versioning = no
    with bake_in_temp_dir(cookies, extra_context={"contribution_name": "test",
                                                  "use_dynamic_versioning": "no"}) as result:
        with open(result.project / 'pyproject.toml') as file:
            content = file.read()
        assert 'dynamic = ["version"]' not in content
        assert 'version = "0.1.0"' in content
        assert 'requires = ["setuptools", "setuptools_scm"]' not in content
        assert '[tool.setuptools_scm]' not in content


def test_github_actions_removal(cookies):
    with bake_in_temp_dir(cookies, extra_context={"contribution_name": "test",
                                                  "use_github_actions": "no"}) as result:
        assert check_construct(result)
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert '.github' not in found_toplevel_files


def test_precommit_hooks_file_removal(cookies):
    with bake_in_temp_dir(cookies, extra_context={"contribution_name": "test",
                                                  "use_pre_commit_hooks": "no"}) as result:
        assert check_construct(result)
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert '.pre-commit-config.yaml' not in found_toplevel_files


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


def test_theorist(cookies):
    with bake_in_temp_dir(cookies, extra_context={"contribution_name": "test-theorist",
                                                  "autora_contribution_type": "theorist",
                                                  }) as result:
        assert check_construct(result)

        # Check naming of directory
        assert 'autora-theorist-test-theorist' == os.path.basename(result.project)

        # Check source code tree structure
        l_tree = tree_list(result.project / 'src')
        l_tree = [s.split(os.path.basename(result.project))[1] for s in l_tree]
        assert l_tree == ['/src/autora',
                          '/src/autora/theorist',
                          '/src/autora/theorist/test_theorist',
                          '/src/autora/theorist/test_theorist/__init__.py']


def test_experimentalist(cookies):
    subtypes_raw = [
        "{% if cookiecutter.autora_contribution_type == 'experimentalist' -%}sampler{% else -%}N/A - Press Enter to Skip{% endif -%}",
        "{% if cookiecutter.autora_contribution_type == 'experimentalist' -%}pooler{% else -%}N/A - Press Enter to Skip{% endif -%}",
        "{% if cookiecutter.autora_contribution_type == 'experimentalist' -%}custom{% else -%}N/A - Press Enter to Skip{% endif -%}"]
    subtypes = ['sampler', 'pooler', 'custom']

    d_subtypes = {}
    for i, (subtype, raw) in enumerate(zip(subtypes, subtypes_raw)):
        d_inputs = {"contribution_name": "test-experimentalist",
                    "autora_contribution_type": "experimentalist",
                    "__experimentalist_type": raw
                    }
        if subtype == 'custom':
            d_inputs['custom_experimentalist_type'] = 'new-type'

        with bake_in_temp_dir(cookies, extra_context=d_inputs) as result:
            assert check_construct(result)

            # Check source code tree structure
            basename = os.path.basename(result.project)
            l_tree = tree_list(result.project / 'src')
            l_tree = [s.split(basename)[1] for s in l_tree]

            # Add to dict
            d_subtypes[subtype] = {'basename': basename, 'tree': l_tree}

    # Check directory names
    assert d_subtypes['sampler'][
               'basename'] == 'autora-experimentalist-sampler-test-experimentalist'
    assert d_subtypes['pooler'][
               'basename'] == 'autora-experimentalist-pooler-test-experimentalist'
    assert d_subtypes['custom'][
               'basename'] == 'autora-experimentalist-new-type-test-experimentalist'

    # Check directory trees
    assert d_subtypes['sampler']['tree'] == ['/src/autora', '/src/autora/experimentalist',
                                             '/src/autora/experimentalist/sampler',
                                             '/src/autora/experimentalist/sampler/test_experimentalist',
                                             '/src/autora/experimentalist/sampler/test_experimentalist/__init__.py']

    assert d_subtypes['pooler']['tree'] == ['/src/autora', '/src/autora/experimentalist',
                                            '/src/autora/experimentalist/pooler',
                                            '/src/autora/experimentalist/pooler/test_experimentalist',
                                            '/src/autora/experimentalist/pooler/test_experimentalist/__init__.py']

    assert d_subtypes['custom']['tree'] == ['/src/autora', '/src/autora/experimentalist',
                                            '/src/autora/experimentalist/new_type',
                                            '/src/autora/experimentalist/new_type/test_experimentalist',
                                            '/src/autora/experimentalist/new_type/test_experimentalist/__init__.py']


def test_runner(cookies):
    subtypes_raw = [
        "{% if cookiecutter.autora_contribution_type == 'experiment_runner' -%}experiment_runner{% else -%}N/A - Press Enter to Skip{% endif -%}",
        "{% if cookiecutter.autora_contribution_type == 'experiment_runner' -%}experimentation_manager{% else -%}N/A - Press Enter to Skip{% endif -%}",
        "{% if cookiecutter.autora_contribution_type == 'experiment_runner' -%}recruitment_manager{% else -%}N/A - Press Enter to Skip{% endif -%}"]
    subtypes = ['experiment_runner', 'experimentation_manager', 'recruitment_manager']

    d_subtypes = {}
    for i, (subtype, raw) in enumerate(zip(subtypes, subtypes_raw)):
        d_inputs = {"contribution_name": "test_runner",
                    "autora_contribution_type": "experiment_runner",
                    "experiement_runner_type": raw
                    }

        with bake_in_temp_dir(cookies, extra_context=d_inputs) as result:
            assert check_construct(result)

            # Check source code tree structure
            basename = os.path.basename(result.project)
            l_tree = tree_list(result.project / 'src')
            l_tree = [s.split(basename)[1] for s in l_tree]

            # Add to dict
            d_subtypes[subtype] = {'basename': basename, 'tree': l_tree}

    # Check directory names
    assert d_subtypes['experiment_runner'][
               'basename'] == 'autora-experiment_runner-test_runner'
    assert d_subtypes['experimentation_manager'][
               'basename'] == 'autora-experiment_runner-experimentation_manager-test_runner'
    assert d_subtypes['recruitment_manager'][
               'basename'] == 'autora-experiment_runner-recruitment_manager-test_runner'

    # Check directory trees
    assert d_subtypes['experiment_runner']['tree'] == ['/src/autora',
                                                       '/src/autora/experiment_runner',
                                                       '/src/autora/experiment_runner/test_runner',
                                                       '/src/autora/experiment_runner/test_runner/__init__.py']

    assert d_subtypes['experimentation_manager']['tree'] == ['/src/autora',
                                                             '/src/autora/experiment_runner',
                                                             '/src/autora/experiment_runner/experimentation_manager',
                                                             '/src/autora/experiment_runner/experimentation_manager/test_runner',
                                                             '/src/autora/experiment_runner/experimentation_manager/test_runner/__init__.py']

    assert d_subtypes['recruitment_manager']['tree'] == ['/src/autora',
                                                         '/src/autora/experiment_runner',
                                                         '/src/autora/experiment_runner/recruitment_manager',
                                                         '/src/autora/experiment_runner/recruitment_manager/test_runner',
                                                         '/src/autora/experiment_runner/recruitment_manager/test_runner/__init__.py']


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
        l_tree = [s.split(basename)[1] for s in l_tree]

        assert basename == 'autora-new_type-test_custom'
        assert l_tree == ['/src/autora',
                          '/src/autora/new_type',
                          '/src/autora/new_type/test_custom',
                          '/src/autora/new_type/test_custom/__init__.py']
