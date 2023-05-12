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
