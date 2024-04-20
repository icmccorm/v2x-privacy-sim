import scripts.diff as diff
import numpy
origin = (0, 0)

def distance(point_1, point_2):
    return numpy.sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)

def csv_row(mode, budget, value):
    return f"{mode},{budget},{value}\n"

if __name__ == "__main__":

    with open("./noise_cost.csv", "w") as measurements:

        for budget_step in range(0, 1001, 1):
            # privacy level 
            budget = budget_step / 1000
            
            # "uncertainty" arrays
            distance_measurements = []
            heading_measurements = []
            
            for i in range(0, 100):
                arbitrary = diff.Arbitrary(budget, 2 * numpy.pi)
                noised_heading = arbitrary.apply_noise(origin)

                positional = diff.Positional(budget)
                noised_position = positional.apply_noise(origin)

                noised_distance_distance = distance(origin, noised_position)
                noised_heading_distance = distance(origin, noised_heading)

                measurements.write(csv_row("distance", budget, noised_distance_distance))
                measurements.write(csv_row("heading", budget, noised_heading_distance))



