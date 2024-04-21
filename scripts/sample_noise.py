import diff as diff
import numpy as np
origin = (0, 0)

def distance(point_1, point_2):
    return np.sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)

def csv_row(mode, budget, value):
    return f"{mode},{budget},{value}\n"

measurements.write(csv_row("mode", "budget", "distance"))
for budget_step in range(0, 10000, 1):
    for i in range(0, 10):
        positional_budget = budget_step
        positional = diff.Positional(positional_budget, 100)
        noised_position = positional.sample()
        noised_distance_distance = distance(origin, noised_position)
        measurements.write(csv_row("distance", positional_budget, noised_distance_distance))
        angular = diff.Arbitrary(positional_budget, 90, filter=lambda a: (np.clip(a[0],0, 180), np.clip(a[1], 0, 180) ))
        angular_noise = angular.sample()
        heading_distance = distance(origin, angular_noise)
        measurements.write(csv_row("heading", positional_budget, heading_distance))
measurements.close()

