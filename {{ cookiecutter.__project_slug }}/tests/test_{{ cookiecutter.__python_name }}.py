{% if cookiecutter.__autora_contribution_type == "theorist" -%}
from autora.{{ cookiecutter.__full_path.lower().replace('/','.') }} import ExampleRegressor

def test():
    theorist = ExampleRegressor()
    assert theorist is not None
{% elif cookiecutter.__autora_contribution_type == "experimentalist" -%}
{% if cookiecutter.__contribution_subtype == "sampler" -%}
from autora.{{ cookiecutter.__full_path.lower().replace('/','.') }} import example_sampler
import numpy as np

def test_output_dimensions():
    X = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    n = 2
    X_new = example_sampler(X, n)

    # Check that the sampler returns n experiment conditions
    assert X_new.shape == (n, X.shape[1])
{% elif cookiecutter.__contribution_subtype == "pooler" -%}
from autora.{{ cookiecutter.__full_path.lower().replace('/','.') }} import example_pool



def test_identity():
    sample = example_pool(2.0)
    assert sample == 2.0
{% endif -%}
{% else -%}
from autora.{{ cookiecutter.__full_path.lower().replace('/','.') }} import function_to_test

def test():
    outcome = function_to_test
    assert outcome == expected_outcome
{% endif %}

# Note: We encourage you to adjust this test and write more tests.
