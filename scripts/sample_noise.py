import diff as diff
import numpy as np
import math

def distance(point_1, point_2):
    return np.sqrt((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)

def csv_row(mode, budget, value):
    return f"{mode},{budget},{value}\n"

def heading_to_angle(x_heading, y_heading):
    """Function which converts the two heading vector components to an angle measured in degrees (0° - 360°)

    Parameters
    ----------
    x_heading : double, required
        The first vector component of the BSM message heading

    y_heading : double, required
        The second vector component of the BSM message heading

    Returns
    -------
    angle : double
        True if the value1 is between value2 - tolerance and value2 + tolerance
        
    """
    det = -y_heading
    dot = x_heading
    angle = math.atan2(det, dot) * 180 / math.pi

    if x_heading >= 0 and y_heading > 0:
        angle = 360 + angle
    elif x_heading < 0 and y_heading >= 0:
        angle = 360 + angle
    return angle


# budget type: position_budget, speed_budget, angle_budget
def init_NoiseMachine(eps_elem, budget_type):
    if budget_type == "positional":
        noise = diff.NoiseMachine(position_budget = eps_elem[0], speed_budget = 0, angle_budget = 0)
    elif budget_type == "speed":
        noise = diff.NoiseMachine(position_budget = 0, speed_budget = eps_elem[1], angle_budget = 0)
    elif budget_type == "angle":
        noise = diff.NoiseMachine(position_budget = 0, speed_budget = 0, angle_budget = eps_elem[2])
    elif budget_type == "comb":
        noise = diff.NoiseMachine(position_budget = eps_elem[0], speed_budget = eps_elem[1], angle_budget = eps_elem[2])
    return noise 


# POSITION TOLERANCE
POS_TOLERANCE = 20
# HEADING TOLERANCE
ANGLE_TOLERANCE = 45

BUDGET_TYPE = "positional"

if __name__ == "__main__":

    position = (0, 0)
    heading = (0.212621, 0.977135) # random sample
    speed = (0.16358310664810494, 0.3168009495830433) # ave from pc_1/rsu[0]

    # positional noise budget
    positional_range = np.arange(0.08, 8.08, 0.08)
    # speed noise budget 
    speed_range = np.arange(0.001, 0.1001, 0.001)
    # heading noise budget 
    heading_range = np.arange(0.001, 0.1001, 0.001)
    # zip epsilons
    epsilon_zip = list(zip(positional_range, speed_range, heading_range))

    average_uncertainty = []
    stddev_uncertainty = []
    
    # for each element of epsilon 
    for budget_step in epsilon_zip:
        # define noise given 
        noise = init_NoiseMachine(eps_elem=budget_step, budget_type=BUDGET_TYPE)
        orig_pos = []
        noisy_pos = []        
        # itera
        for i in range(0, 10): # 1000
            
            # take t+5 position using original data
            orig_angle = heading_to_angle(heading[0], heading[1])
            orig_rad = math.radians(orig_angle)
            orig_speed = np.sqrt(speed[0]**2 + speed[1]**2)
            orig_dist = orig_speed * 5 # arbitrary value
            orig_heading_2 = (None,None)
            orig_heading_2[0] = position[0] + (orig_dist * np.cos(orig_rad))
            orig_heading_2[1] = position[1] + (orig_dist * np.sin(orig_rad))

            # noisy values
            noisy_position = (None, None)
            noisy_speed = None 
            noisy_angle = None

            # positional noise
            noise_x, noise_y = noise.position.sample()
            noisy_position[0] = position[0] + noise_x
            noisy_position[1] = position[1] + noise_y
            # heading noise
            noisy_angle = orig_angle + noise.angle.sample(2*ANGLE_TOLERANCE, 2*ANGLE_TOLERANCE) % 360
            noisy_rad = math.radians(noisy_angle)
            # speed noise 
            speed_range = 32.38587899036572 # np.ptp(events['speed']) --> using full pc_1/rsu[0]bsm.csv
            noisy_speed = orig_speed + noise.speed.sample(speed_range, speed_range)
            noisy_dist = noisy_speed * 5 # arbitrary value

            # take t+5 position using noisy data
            noisy_position_2 = (None, None)
            noisy_position_2[0] = noisy_position[0] + (noisy_dist * np.cos(noisy_rad))
            noisy_position_2[1] = noisy_position[1] + (noisy_dist * np.sin(noisy_rad))

            # append to episode arrays
            orig_pos.append(orig_heading_2)
            noisy_pos.append(noisy_position_2)

        # measure distance between t+5 original vs. noisy data    
        diff_pos_transformation = np.linalg.norm(np.array(noisy_pos) - np.array(orig_pos), axis=1)
        # mean
        diff_pos_mean = np.mean(diff_pos_transformation)
        average_uncertainty.append(diff_pos_mean)
        # standard dev
        diff_pos_std = np.std(diff_pos_transformation)
        stddev_uncertainty.append(diff_pos_std)

        print(diff_pos_mean)
        break



    #         positional_budget = budget_step
    #         positional = diff.Positional(positional_budget, 100)
    #         noised_position = positional.sample()
    #         noised_distance_distance = distance(origin, noised_position)
    #         # measurements.write(csv_row("distance", positional_budget, noised_distance_distance))
    #         angular = diff.Arbitrary(positional_budget, 90, filter=lambda a: (np.clip(a[0],0, 180), np.clip(a[1], 0, 180) ))
    #         angular_noise = angular.sample()
    #         heading_distance = distance(origin, angular_noise)
    #         # measurements.write(csv_row("heading", positional_budget, heading_distance))
    # # measurements.close()

