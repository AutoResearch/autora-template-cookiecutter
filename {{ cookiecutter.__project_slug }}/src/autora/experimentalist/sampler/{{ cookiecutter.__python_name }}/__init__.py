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
        These examples add documentations and also work as doctests
        >>> example_sampler([1, 2, 3, 4])
        1
        >>> example_sampler(range(3, 10))
        3

    """
    if num_samples is None:
        num_samples = condition_pool.shape[0]

    new_conditions = condition_pool

    return new_conditions[:num_samples]
