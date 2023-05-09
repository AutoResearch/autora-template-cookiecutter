# AutoRA Template

## Quickstart Guide

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

Use `pip install` to install the current project (`"."`) in editable mode (`-e`) with dev-dependencies (`[dev]`):
```shell
pip install -e ".[dev]"
```

*Note: You may install new dependencies via ``pip install packagename`` inside your virtual environment. If those
dependencies are vital to your package, you will have to add them to the ``pyproject.toml`` (see Step 6 of the 
Contribution Guide).*

## Contribution Guide 

### Step 1: Choose Feature Category

First you have to choose **which type of feature** you would like to add to AutoRA. There are four categories of contributions:<br>

(1)  **Theorist**: An sklearn regressor that returns an interpretable model relating experiment conditions $X$ to 
observations $Y$.<br>
*Example: The [Bayesian Machine Scientist](https://github.com/AutoResearch/autora-theorist-bms) (Guimerà et al., 2020, 
in Science Advances) returns an equation governing the relationship between $X$ and $Y$.* <br>

(2)  **Experimentalist**: A method that identifies novel experiment conditions $X'$ that yield scientific merit. 
Experimentalists may either be implemented as a *pooler* (generating a pool of novel experiment conditions) or as a 
sampler (selecting from an existing pool of experiment conditions $X$).<br>
*Example: The [Novelty Sampler](https://github.com/AutoResearch/autora-novelty-sampler) selects novel experiment 
conditions $X'$ with respect to a pairwise distance metric applied to existing experiment conditions $X$.*
<br>

(3) **Experiment Runners**: A method that orchestrates the collecting of observations for a given set of 
experiment conditions.<br>
*Example: The [Firebase-Prolific Runner](https://github.com/AutoResearch/autora-experiment-runner-firebase-prolific) 
enables the collection of behavioral data from human participants via web-based experiments hosted on 
[Firebase](https://firebase.google.com/), using a pool of participants registered through
[Prolific](https://www.prolific.co/).* <br>

(3) **Synthetic Data**: A ground-truth model that implements a hypothesized relationship between experimental conditions
$X$ and observations $Y$. Synthetic models may act as objects of study for which the underlying mechanisms are known, 
and be used for benchmarking theorists and experimentalists in AutoRA in terms of
their ability to recover the underlying model from synthetic data, e.g., by acting as "synthetic participants".
*Example: The basic [Synthetic Data Package](https://github.com/AutoResearch/autora-synthetic-data) implements simple 
models of economic choice and psychophysics.*

### Step 2: Delete Irrelevant Files

Depending on which feature you want to contribute, you can remove initialization files from all irrelevant features.
You may delete the following initialization files from the template:

- Theorist: ``src/autora/theorist/example_theorist/__init__.py``
- Experimentalist (Pooler): ``src/autora/experimentalist/pooler/example_pooler/__init__.py``
- Experimentalist (Sampler): ``src/autora/experimentalist/sampler/example_sampler/__init__.py``
- Experiment Runner: ``src/autora/experiment_runner/example_runner/__init__.py``
- Synthetic Data: ``src/autora/synthetic/example_data/__init__.py``

In addition, you may delete the following test files from the template:

- Theorist: ``tests/test_theorist_example.py``
- Experimentalist (Pooler): ``tests/test_experimentalist_pooler_example.py``
- Experimentalist (Sampler): ``tests/test_experimentalist_sampler_example.py``

For instance, if you would like to implement an experimentalist sampler, then you may remove all files listed above 
except for 
- ``src/autora/experimentalist/sampler/example_sampler/__init__.py`` and 
- ``tests/test_experimentalist_sampler_example.py``.

### Step 3: Implement Your Code

You may now add a folder in the respective feature category. For instance, if you would like to implement
and experimentalist sampler, then you may rename the subfolder ``example_sampler`` in 
``src/autora/experimentalist/sampler/`` and add your implementation of the sampler in the ``__init__.py`` file. You may 
also add additional files in this folder. Just make sure to import the core function or class of your feature
in the ``__init__.py''' if it is implemented elswhere. 

*Note: You can create folders for new categories if none of the existing feature categories seems fitting.*

### Step 4 (Optional): Add Tests

It is highly encouraged to add unit tests to ensure your code is working as intended. These can be [doctests](https://docs.python.org/3/library/doctest.html) or as test cases in `tests/test_your_contribution_name.py`.
For example, if you are implementing an experiment sampler, you may rename and modify the 
``tests/test_experimentalist_sampler_example.py``.

*Note: Tests are required if you wish that your feature becomes part of the main 
[autora](https://github.com/AutoResearch/autora) package. However, regardless of whether you choose to implement tests, 
you will still be able to install your package separately, in addition to autora.* 

### Step 5 (Optional): Add Documentation

It is highly encouraged that you add documentation of your package in your `docs/index.md`. You can also add new pages 
in the `docs` folder. Update the `mkdocs.yml` file to reflect structure of the documentation. For example, you can add 
new pages or delete pages that you deleted from the `docs` folder.

*Note: Docmentation is required if you wish that your feature becomes part of the main 
[autora](https://github.com/AutoResearch/autora) package. However, regardless of whether you choose to write
documentation, you will still be able to install your package separately, in addition to autora.*

### Step 6: Add Dependencies

In pyproject.toml add the new dependencies under `dependencies`

Install the added dependencies
```shell
pip install -e ".[dev]"
```

### Step 7: Publish Your Package

Once your project is implemented, you may publish it as subpackage of AutoRA. If you have not thoroughly vetted your project or would otherwise like to refine it further, you may 
nervous about the state of your package–you will be able to publish it as a pre-release, indicating to users that
the package is still in progress.

#### Step 7.1: Update Metadata

To begin publishing your package, update the metadata under `project` in the pyproject.toml file to include 
- name, 
- description, 
- author-name, 
- author-email, and 
- version.

Also, update the URL for the repository under `project.urls`.

There are at least two options for publishing the package. For beginners, we recommend Option 1 (via Github Actions) 
as it is easier to follow.

#### Step 7.2 (Option 1): Publish via GitHub Actions

To automate the publishing process for your package, you can use a GitHub action instead of Twine:
- Add the GitHub action to the `.github/workflows` directory: For example, you can use the default publishing action:
  - Navigate to the `actions` on the GitHub website of your repository.
  - Search for the `Publish Python Package` action and add it to your project
- Create a new release: Click on `create new release` on the GitHub website of your repository.
- Choose a tag (this is the version number of the release. If you didn't set up dynamic versioning it should match the version in the `pyproject.toml` file)
- Generate release notes automatically by clicking `generate release`, which adds the markdown of the merged pull requests and the contributors.
- If this is a pre-release check the box `set as pre-release`
- Click on `publish release`


#### Step 7.2 (Option 2): Publish via Twine

You can follow the guide here: https://packaging.python.org/en/latest/tutorials/packaging-projects/
 
Then, build the package using:
```shell
python -m build
```

Publish the package to PyPI using `twine`:
```shell
twine upload dist/*
```


#### Step 7.3 (Optional): Dynamic Versioning
To automatically generate the version number for each release, you can use dynamic versioning instead of updating the version number manually. To set this up, you need to alter the `pyproject.toml` file:
- Replace `version = "..."` with `dynamic = ["version"]` under `project`
- Replace the `build-system` section with the following:
```toml
[build-system]
requires = ["setuptools", "setuptools_scm"]
build-backend = "setuptools.build_meta"
```
- Add a new section to the `pyproject.toml` file:
```toml
[tool.setuptools_scm]
```
#### Dynamic Versioning: Publishing via GitHub Actions
You can use dynamic versioning with the GitHub action described in the previous section. The workflow remains the same, 
but you don't have to update the version in the `pyproject.toml` file.

#### Dynamic Versioning: Publishing Using `twine`
If you are using dynamic versioning with Twine, follow these steps to publish your package:
- Commit all of your changes.
- Tag the commit: Create an annotated Git tag at the commit you want to release. This is typically the most recent 
commit on your main branch. For example, you can run `git tag -a 1.0.0a` to create a tag named "1.0.0a" at the 
current commit.
- Build and release the package using Twine as described in the above section.
 
## Questions & Help

If you have any questions or require any help, please add your question in the 
[Contributer Q&A of AutoRA Discussions](https://github.com/orgs/AutoResearch/discussions/categories/contributor-q-a).
We look forward to hearing from you!
