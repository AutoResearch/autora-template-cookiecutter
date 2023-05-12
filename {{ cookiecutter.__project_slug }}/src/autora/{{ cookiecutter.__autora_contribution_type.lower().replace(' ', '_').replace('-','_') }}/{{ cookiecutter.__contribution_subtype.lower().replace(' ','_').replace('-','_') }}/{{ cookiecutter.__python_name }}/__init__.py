{% if cookiecutter.__autora_contribution_type == "theorist" -%}
"""
Example Theorist
"""


from sklearn.base import BaseEstimator


class ExampleRegressor(BaseEstimator):
    """
    Include inline mathematics in docstring \\(x < 1\\) or $c = 3$
    or block mathematics:

    \\[
        x + 1 = 3
    \\]


    $$
    y + 1 = 4
    $$

    """

    def __init__(self):
        pass

    def fit(self, conditions, observations):
        pass

    def predict(self, conditions):
        pass
{% elif cookiecutter.__autora_contribution_type == "experimentalist" -%}
{% if cookiecutter.__contribution_subtype == "sampler" -%}
"""
Example Experimentalist Sampler
"""


import numpy as np
from typing import Optional

def example_sampler(
    condition_pool: np.ndarray, num_samples: Optional[int] = None) -> np.ndarray:
    """
    Add a description of the sampler here.

    Args:
        condition_pool: pool of experimental conditions to evaluate
        num_samples: number of experimental conditions to select

    Returns:
        Sampled pool of experimental conditions

    *Optional*
    Examples:
        These examples add documentation and also work as tests
        >>> example_sampler([1, 2, 3, 4])
        1
        >>> example_sampler(range(3, 10))
        3

    """
    if num_samples is None:
        num_samples = condition_pool.shape[0]

    new_conditions = condition_pool

    return new_conditions[:num_samples]
{% elif cookiecutter.__contribution_subtype == "pooler" -%}
"""
Example Experimentalist Pooler
"""


def example_pool(argument: float) -> float:
    """
    Add a description of the pooler here

    Args:
        argument: description of the argument
    Returns: pool of experimental conditions

    *Optional*
    Examples:
        These examples add documentation and also work as tests
        >>> example_pool(1.)
        1.0
    """
    new_conditions = argument

    return new_conditions
{% elif cookiecutter.__contribution_subtype != "not-applicable" -%}
"""
Example Experimantalist {{ cookiecutter.custom_experimentalist_type }}
"""


def example(argument: float) -> float:
    """
    Add a description here
    Args:
        argument: description of the argument
    Returns: description of the return value

    *Optinal*
    Examples: 
        These examples add documentation and alsow work as tests
        >>> example(1.)
        1.0
    """
    return argument
{% endif -%}
{% elif cookiecutter.__autora_contribution_type == "experiment_runner" -%}
{% if cookiecutter.__contribution_subtype != "experiment_runner" -%}
"""
Example Experiment Runner
"""


def example_runner(conditions):
    """
    Add a description of the experiment runner here

    Args:
        conditions: list of conditions to get observations for
    Returns: observations

    """
    observations = conditions

    return observations
{% elif cookiecutter.__contribution_subtype == "experimentation_manager" -%}
"""
Example Experimentation Manager

    These are example functions that could be included 
    (but are not necessarily included)
"""


def send_conditions(args, conditions):
    """
    Add a description here
    Args:
        args: the arguments needed to set up the experiment (e.g., credentials)
        conditions: the conditions to be sent
    """
    pass


def check_status(args):
    """
    Add description here
    """
    pass


def get_observations(args):
    """
    Add description here
    """
    observations = None
    return observations
{% elif cookiecutter.__contribution_subtype == "recruitment_manager" -%}
"""
Example Recruitment Manager

    These are example functions that could be included 
    (but are not necessarily included)
"""


def example_setup_recruitment(args):
    """
    Add your description here.
    Set up a study on an example recruitment platform.
    
    Args:
        the arguments needed to set up the study (e.g., credentials)
    """
    pass


def start_recruitment(args):
    """
    Add description here.
    Start the recruitment on an example recruitment platform.

    Args:
        the arguments needed to start the recruitment (e.g., credentials)
    """
    pass


def pause_recruitment(args):
    """
    Add description here.
    Pause the recruitment on an example recruitment platform.

    Args:
        the arguments needed to start the recruitment (e.g., credentials)
    """


def check_recruitment_status(args):
    """
    Add description here.
    Get information on the status of recruitment for a study on an example recruitment platform.
    
    Args:
        the arguments needed to start the recruitment (e.g., credentials)
    """
    pass
{% endif -%}
{% elif cookiecutter.__autora_contribution_type == "synthetic_data" -%}
""" 
Example Synthetic Data

"""
{% else -%}
"""
Example {{ cookiecutter.__autora_contribution_type }}
{% endif -%}
