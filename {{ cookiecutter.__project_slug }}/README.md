# AutoRA Template

## Quickstart Guide

### Create GitHub Repository

You should create a GitHub repository from the root folder of this project:
- Create a new repository on GitHub (a sensible name for the repository would be {{ cookiecutter.__project_slug }})
- Follow the guide under `…or push an existing repository from the command line
` 

### Virtual Environment 
Install this in an environment using your chosen package manager. In this example we are using virtualenv

Install:
- python (3.8 or greater): https://www.python.org/downloads/
- virtualenv: https://virtualenv.pypa.io/en/latest/installation.html

Create a new virtual environment:
```shell
virtualenv venv
```
*Note: You want to ensure that the python version matches that of autora. If necessary 
you can specify the respective python version directly, e.g., ``virtualenv venv --python=python3.9``*

Activate it:
```shell
source venv/bin/activate
```

### Install Dev Dependencies

Use `pip install` to install the current project (`"."`) in editable mode (`-e`) with dev-dependencies (`[dev]`):
```shell
pip install -e ".[dev]"
```

*Note: You may install new dependencies via ``pip install packagename`` inside your virtual environment. If those
dependencies are vital to your package, you will have to add them to the ``pyproject.toml`` (see Step 6 of the 
Contribution Guide).*

## Contribution Guide

{% if cookiecutter.__contrib_type_modulename == "theorist" -%}
### Theorist
An sklearn regressor that returns an interpretable model relating experiment conditions $X$ to 
observations $Y$.<br>
*Example: The [Bayesian Machine Scientist](https://github.com/AutoResearch/autora-theorist-bms) (Guimerà et al., 2020, 
in Science Advances) returns an equation governing the relationship between $X$ and $Y$.* <br>
{% elif cookiecutter.__contrib_type_modulename == "experimentalist" -%}
### Experimentalist
A method that identifies novel experiment conditions $X'$ that yield scientific merit.
*Example: The [Novelty Experimentalist](https://github.com/AutoResearch/autora-experimentalist-novelty) selects novel experiment 
conditions $X'$ with respect to a pairwise distance metric applied to existing experiment conditions $X$.*
{% elif cookiecutter.__contrib_type_modulename == "experiment_runner" -%}
### Experiment Runners
A method that orchestrates the collecting of observations for a given set of 
experiment conditions, which may include the recruitment of participants.<br>
*Example: The [Firebase-Prolific Runner](https://github.com/AutoResearch/autora-experiment-runner-firebase-prolific) 
enables the collection of behavioral data from human participants via web-based experiments hosted on 
[Firebase](https://firebase.google.com/), using a pool of participants registered through
[Prolific](https://www.prolific.co/).* <br>
{% if cookiecutter.__contrib_subtype_modulename == "recruitment_manager" -%}
*Recruitment Manager* is a method (or collection of methods) to recruit participants.<br>
*Example: The [Prolific Recruitment Manager](https://github.com/AutoResearch/autora-experiment-runner-recruitment-manager-prolific)
enables the recruitment of participants via Prolific.*
{% elif cookiecutter.__contrib_subtype_modulename == "experimentation_manager" -%}
*Experimentation Manager* is a method (or collection of methods) to handle the requisite experimentation processes.<br>
*Example: The [Firebase Experimentation Manager](https://github.com/AutoResearch/autora-experiment-runner-experimentation-manager-firebase)
enables the hosting of a web-based experiment on Firebase and the storage of conditions and observations via Firestore.*
{% elif cookiecutter.__contrib_subtype_modulename == "synthetic" -%}
*Synthetic*
A ground-truth model that implements a hypothesized relationship between experimental conditions
$X$ and observations $Y$. Synthetic models may act as objects of study for which the underlying mechanisms are known, 
and be used for benchmarking theorists and experimentalists in AutoRA in terms of
their ability to recover the underlying model from synthetic data, e.g., by acting as "synthetic participants".
*Example: The basic [Synthetic Data Package](https://github.com/AutoResearch/autora-synthetic) implements simple models of economic choice and psychophysics.*
{% endif -%}
{% endif -%}

### Step 1: Implement Your Code

You may now add your code to `src/autora/{{ cookiecutter.__full_path }}/__init__.py` file. You may 
also add additional files in this folder. Just make sure to import the core function or class of your feature
in the `__init__.py` if it is implemented elsewhere. 

### Step 2 (Optional): Add Tests

It is highly encouraged to add unit tests to ensure your code is working as intended. These can be [doctests](https://docs.python.org/3/library/doctest.html) or test cases in `tests/test_{{ cookiecutter.__contrib_name_modulename }}.py`.

*Note: Tests are required if you wish that your feature becomes part of the main 
[autora](https://github.com/AutoResearch/autora) package. However, regardless of whether you choose to implement tests, 
you will still be able to install your package separately, in addition to autora.* 

### Step 3 (Optional): Add Documentation

It is highly encouraged that you add documentation of your package in your `docs/index.md`. You can also add new pages 
in the `docs` folder. Update the `mkdocs.yml` file to reflect structure of the documentation. For example, you can add 
new pages or delete pages that you deleted from the `docs` folder.

*Note: Documentation is required if you wish that your feature becomes part of the main 
[autora](https://github.com/AutoResearch/autora) package. However, regardless of whether you choose to write
documentation, you will still be able to install your package separately, in addition to autora.*

### Step 4: Add Dependencies

In pyproject.toml add the new dependencies under `dependencies`

Install the added dependencies
```shell
pip install -e ".[dev]"
```

### Step 5: Publish Your Package

Once your project is implemented, you may publish it as subpackage of AutoRA. If you have not thoroughly vetted your project or would otherwise like to refine it further, you may 
nervous about the state of your package–you will be able to publish it as a pre-release, indicating to users that
the package is still in progress.

#### Step 5.1: Update Metadata

To begin publishing your package, update the metadata under `project` in the pyproject.toml file to include 
- name
- description
- author-name
- author-email
{% if cookiecutter.__contrib_utilities == "basic" -%}
- version
{% endif -%}


Also, update the URL for the repository under `project.urls`.

{% if cookiecutter.__contrib_utilities == "advanced" -%}
#### Step 5.2 Publish via GitHub Actions

To automate the publishing process for your package, you can use a GitHub action:
- Add a github secret in your repository named PYPI_API_TOKEN, that contains a PyPI token of your account
- Add the GitHub action to the `.github/workflows` directory: For example, you can use the default publishing action:
  - Navigate to the `actions` on the GitHub website of your repository.
  - Search for the `Publish Python Package` action and add it to your project
- Create a new release: Click on `create new release` on the GitHub website of your repository.
- Choose a tag (this is the version number of the release. If you didn't set up dynamic versioning it should match the version in the `pyproject.toml` file)
- Generate release notes automatically by clicking `generate release`, which adds the markdown of the merged pull requests and the contributors.
- If this is a pre-release check the box `set as pre-release`
- Click on `publish release`
{% else -%}
#### Step 5.2: Publish via Twine
You can follow the guide here: https://packaging.python.org/en/latest/tutorials/packaging-projects/
{% if cookiecutter.__contrib_utilities == "advanced" -%}
#### Dynamic versioning
If you are using dynamic versioning with Twine, follow these steps to publish your package:
- Commit all of your changes.
- Tag the commit: Create an annotated Git tag at the commit you want to release. This is typically the most recent 
commit on your main branch. For example, you can run `git tag -a 1.0.0a` to create a tag named "1.0.0a" at the 
current commit.
{% endif -%}
- Build the package using:
```shell
python -m build
```
- Publish the package to PyPI using `twine`:
```shell
twine upload dist/*
```
{% endif -%}

### Step 6: Add the package to [`autora`](https://github.com/autoresearch/autora)
Once your package is working and published, you can **make a pull request** on 
[`autora`](https://github.com/autoresearch/autora) to have it vetted and added to the "parent" package.
To do so, you'll need to clone the parent repository, add your package to it as an optional dependency, and make sure your documentation is imported.
Then create a pull request with the changes to let us know about your contribution.

#### Add the package as optional dependency 
In the `pyproject.toml` file of your cloned [`autora`](https://github.com/autoresearch/autora) package, 
add an optional dependency for your new package in the `[project.optional-dependencies]` section:

```toml
example-contribution = ["autora-example-contribution==1.0.0"]
```

!!! success
    Ensure you include the version number.

Add the example-contribution to be part of the corresponding all-contribution-type dependencies:
```toml
all-contribution-type = [
    ...
    "autora[example-contribution]",
    ...
]
```

### Add documentation from the package repository
Import your documentation in the `mkdocs.yml` of the [`autora`](https://github.com/autoresearch/autora) package:
```yml
- User Guide:
  - Contribution Type:
    - Overview: 'contribution-type/overview.md'
    ...
    - Example Contribution: '!import https://github.com/example-contributor/example-contribution/?branch=v1.0.0&extra_imports=["mkdocs/base.yml"]'
    ...
```

## Questions & Help

If you have any questions or require any help, please add your question in the 
[Contributor Q&A of AutoRA Discussions](https://github.com/orgs/AutoResearch/discussions/categories/contributor-q-a).
We look forward to hearing from you!
