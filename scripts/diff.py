import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
ANGLE_SENSITIVITY = 90

class NoiseMachine():
    def __init__(self, position_budget, speed_budget, angle_budget):
        self.position = Positional(position_budget)
        self.speed = Arbitrary(speed_budget)
        self.angle = Arbitrary(angle_budget)

class Arbitrary():
    def __init__(self, budget):
        self.budget = budget
    def sample(self, sensitivity, bound):
        if self.budget == 0:
            return 0
        elif self.budget < 0:
            raise ValueError("Budget must be non-negative")
        else:
            b = sensitivity / self.budget
            return np.clip(np.random.laplace(scale = b), -bound, bound)

RADIUS_FROM_CAR = 100
MAX_DISTANCE_BETWEEN_POINTS = RADIUS_FROM_CAR * 2
STEP_SIZE = 1e-6
DOUBLE_PRECISION = 10e-16

def epsilon(epsilon_prime):
    q = STEP_SIZE / (MAX_DISTANCE_BETWEEN_POINTS * DOUBLE_PRECISION)
    return epsilon_prime + (1 / STEP_SIZE) *np.log((q + 2*np.exp(epsilon_prime*STEP_SIZE)) / (q - 2*np.exp(epsilon_prime*STEP_SIZE)))

def find_max_value(original):
    threshold = 1e-9
    lower_bound = 0
    upper_bound = original
    while upper_bound - lower_bound > threshold:
        midpoint = (lower_bound + upper_bound) / 2
        function_value = epsilon(midpoint)
        if function_value <= original:
            lower_bound = midpoint
        else:
            upper_bound = midpoint
    return lower_bound

class Positional():
    def __init__(self, budget):
        self.budget = find_max_value(budget)
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
            np.clip(r.real, 0, RADIUS_FROM_CAR)
            x = r.real * np.cos(theta) 
            y = r.real * np.sin(theta)
            return (x, y)