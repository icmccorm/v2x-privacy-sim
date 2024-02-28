import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

class Positional():
    def __init__(self, max_radius, budget):
        self.max_radius = max_radius
        self.budget = budget
    
    def apply_noise(self, point):
        """Applies laplacian noise to a cartesian coordinate for a given privacy budget.

        Parameters
        ----------
        point : (float, float), required
            The cartesian coordinate 

        budget : float, required
            The budget of the laplacian noise
            
        Returns
        -------
        (x, y) : (float, float)
            an offset coordinate (x, y) with laplacian noise applied

        Raises
        ------
        ValueError
            If the budget is negative
        """
        if self.budget == 0:
            return point
        elif self.budget < 0:
            raise ValueError("Budget must be non-negative")
        else:
            random_probability = np.random.uniform()
            inner_term = (random_probability - 1) / np.e
            lambert_result = sp.special.lambertw(inner_term, k=-1)
            radius = (-1 / self.budget) * (lambert_result + 1)
            if self.max_radius is not None:
                radius = self.max_radius - 1 / radius
            theta = np.random.uniform(low=0, high=2 * np.pi)
            x = radius.real * np.cos(theta)
            y = radius.real * np.sin(theta)
            return (point[0] + x, point[0] + y)