import diff 
import numpy as np


# create temp.csv
with open("temp.csv", "w") as file:
    file.write("budget,value\n")
    # iterate over values from 0.8 to 0.9 in increments of 0.001
    for budget in range(1, 40, 1):

        budget = budget * 0.25
        arb = diff.Arbitrary(budget)
        #positional = diff.Positional(budget)
        # take 100 samples of positional noise
        for i in range(100):
            sample = arb.sample(32, 32)
            # get distance from the origin using a new function
            
           # def distance(origin, noised_position):
            #    return np.linalg.norm(np.array(noised_position) - np.array(origin))
            #dist = distance([0, 0], sample)
            # write to file
            file.write("{},{}\n".format(budget, sample))
        