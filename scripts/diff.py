import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

class Arbitrary():
    def __init__(self, budget, sensitivity, filter = lambda a: a):
        self.budget = budget
        self.sensitivity = sensitivity
        self.filter = filter
    def sample(self):
        if self.budget == 0:
            return (0, 0)
        elif self.budget < 0:
            raise ValueError("Budget must be non-negative")
        else:
            b = self.sensitivity / self.budget
            return self.filter((np.random.laplace(scale = b), np.random.laplace(scale = b)))

class Positional():
    def __init__(self, budget):
        self.budget = budget
        if self.budget < 0:
            raise ValueError("Budget must be non-negative")
    def sample(self):
        """Applies laplacian noise to a cartesian coordinate for a given privacy budget.

        Parameters
        ----------
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
            return (0, 0)
        else:
            r =  (-1 / self.budget) * (sp.special.lambertw((np.random.uniform() - 1) / np.e, k=-1) + 1)
            theta = np.random.uniform() * 2 * np.pi
            x = r.real * np.cos(theta)
            # noise in y
            y = r.real * np.sin(theta)
            return (x, y)