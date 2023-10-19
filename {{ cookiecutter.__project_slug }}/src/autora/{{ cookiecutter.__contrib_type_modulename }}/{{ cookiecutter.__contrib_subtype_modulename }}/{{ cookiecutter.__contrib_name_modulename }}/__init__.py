{% if cookiecutter.__contrib_type_modulename == "theorist" -%}
"""
Example Theorist
"""

import numpy as np
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

    def fit(self, conditions: np.ndarray, observations: np.ndarray):
        pass

    def predict(self, conditions: np.ndarray) -> np.ndarray:
        pass
{% elif cookiecutter.__contrib_type_modulename == "experimentalist" -%}
"""
Example Experimentalist
"""
import numpy as np
import pandas as pd

from typing import Union, List


def sample(
        conditions: Union[pd.DataFrame, np.ndarray],
        models: List,
        reference_conditions: Union[pd.DataFrame, np.ndarray],
        num_samples: int = 1) -> pd.DataFrame:
    """
    Add a description of the sampler here.

    Args:
        conditions: The pool to sample from.
            Attention: `conditions` is a field of the standard state
        models: The sampler might use output from the theorist.
            Attention: `models` is a field of the standard state
        reference_conditions: The sampler might use reference conditons
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
        num_samples = conditions.shape[0]

    new_conditions = conditions

    return new_conditions[:num_samples]
{% elif cookiecutter.__contrib_type_modulename == "experiment_runner" -%}
{% if cookiecutter.__contrib_subtype_modulename == "experiment_runner" -%}
"""
Example Experiment Runner
"""
import pandas as pd

from typing import Union


def example_runner(Union[pd.DataFrame, np.ndarray]) -> pd.DataFrame:
    """
    Add a description of the experiment runner here

    Args:
        conditions: list of conditions for which to get observation
    Returns:
        experiment data (a dataframe with conditions and observations)

    """
    experiment_data = conditions

    return experiment_data
{% elif cookiecutter.__contrib_subtype_modulename == "experimentation_manager" -%}
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
{% elif cookiecutter.__contrib_subtype_modulename == "recruitment_manager" -%}
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
{% elif cookiecutter.__contrib_type_modulename == "synthetic_data" -%}
""" 
Example Synthetic Data

"""
{% else -%}
"""
Example {{ cookiecutter.__contrib_type_modulename }}
{% endif -%}
