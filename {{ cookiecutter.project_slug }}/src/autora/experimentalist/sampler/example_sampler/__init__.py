"""
Example Experimentalist Sampler
"""
import numpy as np

def example_sampler(
    condition_pool: np.ndarray, num_samples: int = 1) -> np.ndarray:
    """
    Add a description of the sampler here.

    Args:
        condition_pool: pool of IV conditions to evaluate
        num_samples: number of samples to select

    Returns:
        Sampled pool of conditions

    *Optional*
    Examples:
        These examples add documentations and also work as doctests
        >>> example_sampler([1, 2, 3, 4])
        1
        >>> example_sampler(range(3, 10))
        3

    """
    new_conditions = condition_pool

    return new_conditions[:num_samples]