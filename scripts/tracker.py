#!./env/bin/python
import os
import logging

import math
from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path
# differential privacy
import diff as diff
import pandas as pd
import numpy as np
from tqdm import tqdm

CSV_HEADERS = [
    'position_budget',
    'speed_budget', 
    'heading_budget',
    'fq',
    'pc',
    'prec',
    'recall',
    'f1_score'
]

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# NUMBER OF EAVESDROPPING ANTENNA 
ANTENNA_NUM = 3
# MEAN DISTANCE BETWEEN TWO CONSECUTIVE BSM
MEAN_DISTANCE = 25
# POSITION TOLERANCE
POS_TOLERANCE = 20
# HEADING TOLERANCE
ANGLE_TOLERANCE = 45

# NAME OF THE FILE CONTAINING ALL THE EAVESDROPPED BSM
FILE_NAME = 'rsu[{num}]bsm.csv'

def disable_progress_bars():
    return bool(int(os.environ.get('TQDM_DISABLE', 0)))

def mean_pseudonyms_change(path):
    """Merge all the data in the \'path\' and calculate the average pseudonyms changes.

    Parameters
    ----------
    path : str, required
        The base \'path\' of the data
    
    Returns
    -------
    data-frame : pandas.DataFrame()
        The pandas DataFrame containing all the bsm read
    
    pseudonyms : np.array
        The numpy array containing the unique pseudonyms

    Raises
    ------
    FileNotFoundError
        If no found in path.
    """
    data = []
    for i in range(0, ANTENNA_NUM):
        file_name = f'./{path}/{FILE_NAME.format(num=i)}'
        if os.path.exists(file_name) and os.path.isfile(file_name):
            data.append(pd.read_csv(file_name))
        else:
            logging.error(f'File {file_name} not found')
            raise FileNotFoundError
    data = pd.concat(data, axis=0, ignore_index=True)
    data.sort_values(by='t', inplace=True)
    pseudonyms = np.array(pd.unique(data['pseudonym'].values))
    vehicles_num = len(pd.unique(data['realID'].values))
    pseudonyms_num = len(pseudonyms)

    logging.info(f'TOTAL VEHICLES {vehicles_num}, PSEUDONYMS: {pseudonyms_num}')
    logging.info(f'{bcolors.RED}PSEUDONYMS PER VEHICLE (MEAN): {round((pseudonyms_num/vehicles_num), 2)}{bcolors.RESET}')

    return data, pseudonyms

def pseudonym_change_events(dataframe, pseudonyms, noise):
    """This function perform the following actions:
        - Labeling process of the dataset retrieving the entry and exit events of the pseudonyms.
        - Remove for each pseudonym all the unnecessary BSM between the entry.
        - Calculate the degree angle starting from the heading field of the BSM message
        - Calculate the resultant of the speed vector of the BSM message

    Parameters
    ----------
    data-frame : pandas.DataFrame, required
        The pandas data-frame which contains all the bsm eavesdropped by the antennas

    pseudonyms : np.array, required
        The numpy array which contains the unique pseudonyms retrieved from the \'mean_pseudonyms_change\' function
    
    Returns
    -------
    data-frame : pandas.DataFrame()
        The updated pandas DataFrame which include three new columns:
        - \'event\' column representing the BSM message classes (entry event -> e, exit event -> x)
        - \'angle\' column representing the BSM message angle starting from the two heading field
        - \'speed\' column representing the resultant speed starting from the two vector component of the BSM fields
        
    """
    useless_idx = np.empty(0, dtype=int)
    for i in tqdm(pseudonyms.tolist(), disable=disable_progress_bars()):
        pseudonyms_events = dataframe.loc[dataframe['pseudonym'] == i]
        if len(pseudonyms_events) > 1:
            dataframe.loc[pseudonyms_events.iloc[0].name, 'event'] = 'e'
            dataframe.loc[pseudonyms_events.iloc[-1].name, 'event'] = 'x'
            useless_idx = np.append(useless_idx, np.delete(pseudonyms_events.index.values, [0, -1], 0))
        else:
            dataframe.loc[pseudonyms_events.iloc[0].name, 'event'] = 'ex'

    previus_dim = len(dataframe)
    dataframe.drop(useless_idx, inplace=True)
    actual_dim = len(dataframe)

    assert previus_dim != actual_dim, 'DATA-FRAME NOT REDUCED'
    return dataframe

def near(value1, value2, tolerance):
    """Based on the tolerance input calculate if two value are near each other.

    
    Parameters
    ----------
    value1 : double, required
        The first value of the comparison 

    value2 : double, required
        The second value of the comparison 

    tolerance : double, required
        The desired tolerance value
    
    Returns
    -------
    bool
        True if the value1 is between value2 - tolerance and value2 + tolerance
        
    """
    print(f"val1: {value1}, val2: {value2}, tol: {tolerance}")
    return value1 >= (value2 - tolerance) and value1 <= (value2 + tolerance)

    
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

def possible_candidate_found(dataframe, matched_idx, last_seen, results, pseudonyms, to_remove_pseudonyms):
    """This function add the matched pseudonyms to a remove list to and remove the entry and exit events for this specific spedunym from the dataframe. 

    Parameters
    ----------
    data-frame : pandas.DataFrame, required
        The pandas dataframe which contains all the bsm eavesdropped by the antennas

    matched_idx : pandas.index, required
        The pandas dataframe index for the matched BSM message

    last_seen : pandas.DataFrame, required
        The pandas dataframe of one row which contains all the data of the last exit event

    results : dict, required    
        A dictionary containing the key-value of the TP and the FP numbers.

    pseudonyms : np.array, required
        The numpy array which contains the unique pseudonyms retrieved from the \'mean_pseudonyms_change\' function

    to_remove_pseudonyms : np.array, required
        The numpy array which contains all the matched pseudonyms which have to be removed from the original \'pseudonyms\' list 

    Returns
    -------
        pseudonyms : numpy.array
            The numpy array of the remained pseudonyms 


    """
    if dataframe.loc[matched_idx, 'realID'] == last_seen['realID']:
        results['tp'] += 1
    else:
        results['fp'] += 1

    matched_pseudonym = last_seen['pseudonym']
    dataframe.drop(dataframe[dataframe['pseudonym'] == matched_pseudonym].index, inplace=True)
    to_remove_pseudonyms = np.append(to_remove_pseudonyms, np.where(pseudonyms == matched_pseudonym))
    
    return dataframe, to_remove_pseudonyms

def local_change(dataframe, pseudonyms, beacon_interval, results, dimensions=False):
    """
    This function for each pseudonym of the \'pseudonyms\' list perform the following actions:
        - Retrieve the last pseudonym sighting corresponding to the exit event (x)
        - Filter the data-frame searching for entry events occurred between the time of the current exit event and the bsm sending interval plus a 
            time_tolerance which is 50% of the bsm sending interval
        - Apply an optional additional filter if the vehicle dimensions is considered
        - Apply the positional filter which consider the position of the exit event (x) as reference position and search for entry events with similar position considering a tolerance of \'POSITION_TOLERANCE\'
        - Apply the heading filter which consider the new angle column of the data-frame of the exit event (x) as reference value and search for entry events with similar heading considering a tolerance of \'ANGLE_TOLERANCE\'
        - If there are some events after the filter process of the previous step, the algorithm calculate the euclidean distance between the exit event (x) and all the entry event of the plausible matches and sort in descending order considering the euclidean distance.
        - Perform the final check using the \'near\' function:
            - if the difference between the speed*time_difference and the calculated euclidean distance is below the \'tolerance\' value of 2 meters -> True Positive
            - otherwise -> False Positive
        - If none of the plausible events match the previous conditions, the closest event in term of euclidean distance is evaluated considering if the distance il below the \'MEAN_DISTANCE\' threshold
        - Remove all the matched and unmatched pseudonyms for the original list of the pseudonyms

    Parameters
    ----------
    data-frame : pandas.DataFrame, required
        The pandas dataframe which contains all the bsm eavesdropped by the antennas

    pseudonyms : np.array, required
        The numpy array which contains the unique pseudonyms retrieved from the \'mean_pseudonyms_change\' function
    
    beacon_interval : double, required
        The value of the sending message interval which correspond to the inverse of the frequency.
    
    
    results : dict, required
        A dictionary containing the key-value of the TP and the FP numbers.
        
    dimensions : bool, optional
        Boolean value which if is True indicating the use of the vehicle size filter
    
    Returns
    -------
        pseudonyms : numpy.array
            The numpy array of the remained pseudonyms 
    """

    to_remove_pseudonyms = np.empty(0)
    time_tolerance = beacon_interval*0.5
    
    if dimensions:
        logging.info('Using vehicles dimensions as filter')
        if not ('length' in dataframe.columns and 'width' in dataframe.columns):
            logging.error('Columns length and width required')
            raise ValueError
    
    for p in tqdm(pseudonyms.tolist(), disable=disable_progress_bars()):
        last_seen = dataframe.loc[(dataframe['pseudonym'] == p) & (dataframe['event'] == 'x')]

        if last_seen.empty:
            continue
        
        assert len(last_seen) == 1, f'MULTIPLE EXITS EVENTS FOR PSEUDONYM: {p}, {last_seen}'
        
        last_seen = last_seen.iloc[0]
        last_seen_time = last_seen['t']

        possible_match = dataframe.loc[(dataframe['event'] == 'e') | (dataframe['event'] == 'ex')]
        time_interval = possible_match['t'].between(last_seen_time, last_seen_time + beacon_interval + time_tolerance)
        possible_match = possible_match[time_interval]
        
        if dimensions:
            last_seen_width = last_seen['width']
            last_seen_length = last_seen['length']
            possible_match = possible_match.loc[(possible_match['length'] == last_seen_length) & (possible_match['width'] == last_seen_width)]
        
        filter_pos_x = possible_match['pos.x'].between(last_seen['pos.x'] - POS_TOLERANCE, last_seen['pos.x'] + POS_TOLERANCE)
        filter_pos_y = possible_match['pos.y'].between(last_seen['pos.y'] - POS_TOLERANCE, last_seen['pos.y'] + POS_TOLERANCE)
        possible_match = possible_match[(filter_pos_x) & (filter_pos_y)]

        heading_filter = possible_match['angle'].between(last_seen['angle'] - ANGLE_TOLERANCE, last_seen['angle'] + ANGLE_TOLERANCE)
        possible_match = possible_match[heading_filter]
        
        if not possible_match.empty:
            last_pos = np.array((last_seen['pos.x'], last_seen['pos.y'], 0))
            possible_match['distance'] = possible_match.apply(lambda row: np.linalg.norm(last_pos - np.array((row['pos.x'], row['pos.y'], 0))), axis=1)
            possible_match = possible_match.sort_values(by='distance')

            for k in range(len(possible_match)):
                current = possible_match.iloc[k]
                if near(last_seen['speed'] * (current['t'] - last_seen_time), current['distance'], 2):
                    print("found matching speed:")
                    matched_idx = possible_match.iloc[k:k+1].index.values.astype(int)[0]
                    dataframe, to_remove_pseudonyms = possible_candidate_found(dataframe, matched_idx, last_seen, results, pseudonyms, to_remove_pseudonyms)
                    break
            else:
                if possible_match.iloc[0]['distance'] <= MEAN_DISTANCE*beacon_interval:
                    matched_idx = possible_match.iloc[0:1].index.values.astype(int)[0]
                    dataframe, to_remove_pseudonyms = possible_candidate_found(dataframe, matched_idx, last_seen, results, pseudonyms, to_remove_pseudonyms)

    pseudonyms = np.delete(pseudonyms, to_remove_pseudonyms.astype(int))
    return pseudonyms


def local_results(results, fn):
    """Calculate and show the Precision, Recall and F1-Score metrics.

    Parameters
    ----------        
    results : dict, required
        A dictionary containing the key-value of the TP and the FP numbers.
        
    fn : integer, required
        The number representing the False Negative pseudonyms
    
    Returns
    -------
        precision : double
            The precision value

        recall : double
            The recall value 

        f1_score : double
            The F1-Score value 

    """
    tp = results['tp']
    fp = results['fp']
    precision = "NA" if tp + fp == 0 else tp/(tp+fp)
    recall = "NA" if tp + fn == 0 else tp/(tp+fn)
    f1_score = "NA" if precision == "NA" or recall == "NA" or precision + recall == 0 else 2 * ((precision * recall)/(precision + recall))

    f1_score_formatted = f1_score if f1_score == "NA" else '{:.5f}'.format(f1_score)
    precision_formatted = precision if precision == "NA" else '{:.5f}'.format(precision)
    recall_formatted = recall if recall == "NA" else '{:.5f}'.format(recall)

    logging.info(f"{bcolors.GREEN}METRICS -> PRECISION: {precision_formatted}, RECALL: {recall_formatted}, F1 SCORE: {f1_score_formatted}{bcolors.RESET}")
    return precision, recall, f1_score

def filter_dataframe(dataframe, pseudonyms):
    """Function which filter the data-frame by deleting the pseudonyms which occurs only once in the entire data-frame.

    Parameters
    ----------        
        data-frame : pandas.DataFrame, required
            The pandas dataframe which contains all the bsm eavesdropped by the antennas
                    
        pseudonyms : np.array, required
            The numpy array which contains the unique pseudonyms after the \'local_change\' function.

    Returns
    -------
        pseudonyms : np.array, required
            The updated numpy array which contains the unique pseudonyms. 

    """
    vehicles = np.array(dataframe['realID'].unique())
    to_remove_pseudonyms = np.empty(0)

    for v in vehicles.tolist():
        vehicles_pseudonyms = np.array(dataframe.loc[dataframe['realID'] == v]['pseudonym'].unique())
        if len(vehicles_pseudonyms) == 1:
            to_remove_pseudonyms = np.append(to_remove_pseudonyms, np.where(pseudonyms == vehicles_pseudonyms))

    pseudonyms = np.delete(pseudonyms, to_remove_pseudonyms.astype(int))
    return pseudonyms

def analyze(path, freq, dimensions, noise):
    """This function sequentially call all the function of the python script.

    Parameters
    ----------        
        path : str, required
            The directory path where all the files are stored
                    
        freq : int, required
            The sending frequency of the bsm in the simulation.

        dimensions : bool, required
            Boolean value which if is True indicating the use of the vehicle size filter

    Returns
    -------
        precision : double
            The precision value

        recall : double
            The recall value 

        f1_score : double
            The F1-Score value

    """
    logging.info('Pseudonym change mean...')
    dataframe, pseudonyms = mean_pseudonyms_change(path)
    dataframe['speed'] = dataframe.apply(lambda row: np.sqrt(row['speed.x']**2 + row['speed.y']**2), axis=1)
    speed_range = np.ptp(dataframe['speed'])
    logging.info('Getting pseudonym change events...')
    events = pseudonym_change_events(dataframe, pseudonyms, noise)
    
    # apply heading to angle transform
    events['angle'] = events.apply(lambda row: heading_to_angle(row['heading.x'], row['heading.y']), axis=1)

    original_pos = events[['pos.x','pos.y','speed','angle']].copy()
    original_pos["angle_rad"] = list(map(lambda x: math.radians(x), original_pos["angle"]))
    original_pos['distance'] = original_pos['speed'] * freq
    original_pos['pos.x2'] = original_pos['pos.x'] + (original_pos['distance'] * np.cos(original_pos['angle_rad']))
    original_pos['pos.y2'] = original_pos['pos.y'] + (original_pos['distance'] * np.sin(original_pos['angle_rad']))
    logging.debug(f"Original positions:\n----\n{original_pos}\n----\n")

    logging.info('Applying differential privacy to data...')

    for index, row in tqdm(events.iterrows(), total=events.shape[0], disable=disable_progress_bars()):
        noise_x, noise_y = noise.position.sample()
        noise_angle = noise.angle.sample(2*ANGLE_TOLERANCE, 2*ANGLE_TOLERANCE)
        noise_speed = noise.speed.sample(speed_range, speed_range)
        print(noise_speed)
        events.at[index, 'pos.x'] = events.at[index, 'pos.x'] + noise_x
        events.at[index, 'pos.y'] = events.at[index, 'pos.y'] + noise_y
        events.at[index, 'angle'] = events.at[index, 'angle'] + noise_angle
        events.at[index, 'speed'] = events.at[index, 'speed'] + noise_speed

   # calculate distance between original and noised coordinates
    new_pos = events[['pos.x','pos.y','speed','angle']].copy()
    new_pos["angle_rad"] = list(map(lambda x: math.radians(x), new_pos["angle"]))
    new_pos['distance'] = new_pos['speed'] * freq
    new_pos['pos.x2'] = new_pos['pos.x'] + (new_pos['distance'] * np.cos(new_pos['angle_rad']))
    new_pos['pos.y2'] = new_pos['pos.y'] + (new_pos['distance'] * np.sin(new_pos['angle_rad']))

    logging.debug(f"New positions:\n----\n{new_pos}\n----\n")

  #  distance between un-noised and noised transformation 
    diff_pos_transformation = np.linalg.norm(new_pos[['pos.x2', 'pos.y2']].values - original_pos[['pos.x2','pos.y2']].values, axis=1)
    dpt_mean = np.mean(diff_pos_transformation)
    dpt_max = np.max(diff_pos_transformation)
    logging.debug(f"Mean positional noise: {np.mean(diff_pos_transformation)}")

    logging.info('Checking for local pseudonym change...')
    beacon_interval = 1/freq
    
    results = {'tp': 0, 'fp': 0}
    pseudonyms = local_change(events, pseudonyms, beacon_interval, results, dimensions)
    pseudonyms = filter_dataframe(dataframe, pseudonyms)

    fn = len(pseudonyms)
    precision, recall, f1_score = local_results(results, fn)

    return precision, recall, f1_score, dpt_mean, dpt_max

def main(base_folder, freq, policy, dimensions, noise, exp_name):
    """This function compose the complete path using the base_folder, freq and policy and check if the folder actually exist.

    Parameters
    ----------        
        base_folder : str, required
            The base directory path where the data file are stored
        
        freq : int, required
            The desired frequency [1, 2, 5, 10] Hertz

        policy : int, required
            The desired pseudonyms change scheme, which can be [1, 2, 3, 4, 5]
        
        dimensions : bool, required
            Boolean value which indicates if the vehicles size filter will be active or none

    """
    path = f'{base_folder}/fq_{freq}Hz/pc_{policy}'
    path_if_directory(path)
    logging.info(f'Analyze data in \'{path}\'')

    precision, recall, f1_score, dpt_mean, dpt_max = analyze(path, freq, dimensions, noise)
    results = [
        noise.speed.budget,
        noise.position.original_budget,
        noise.position.adjusted_budget,
        noise.angle.budget,
        freq,
        policy,
        precision,
        recall,
        f1_score,
        dpt_mean,
        dpt_max
    ]
    results_file = '{}/run.csv'.format(exp_name)
    print("========= results file: {} ============".format(results_file))
    with open(results_file, 'w') as file:
        file.write(",".join([str(r) for r in results]) + "\n")
    return None

def path_if_directory(s):
    try:
        p = Path(s)
    except (TypeError, ValueError) as e:
        raise ArgumentTypeError(f"Invalid argument '{s}': '{e}'") from e
    
    if not p.is_dir():
        raise ArgumentTypeError(f"'{s}' is not a valid directory path")
    return p

if __name__ == "__main__":
    FORMAT = '\n[%(asctime)s]:[%(levelname)s] %(message)s'
    parser = ArgumentParser()

    parser.add_argument("-q", "--quiet", help="Disable logging", action='store_true')
    parser.add_argument("-d", "--debug", help="Enable debug logging", action='store_true')
    parser.add_argument("-dir", "--directory", help="Specify the base directory", required=True, type=path_if_directory)
    parser.add_argument("-fq", "--freq", help="Insert the desired frequency", required=True, type=int, choices=[1, 2, 5, 10])
    parser.add_argument("-pc", "--policy", help="Insert the desired policy", required=True, type=int, choices=[i for i in range(1,6)])
    parser.add_argument("-dim", "--dimensions", help="Consider vehicles dimensions", action="store_true")
    
    # privacy budget
    parser.add_argument("-pb", "--position-budget", help="Differential privacy budget for position", required=False, type=float, default=0)
    parser.add_argument("-sb", "--speed-budget", help="Differential privacy budget for speed", required=False, type=float, default=0)
    parser.add_argument("-hb", "--heading-budget", help="Differential privacy budget for heading", required=False, type=float, default=0)

    args = parser.parse_args()
    basic_level = logging.DEBUG if args.debug else logging.INFO

    # experiment directory 
    exp_dir_name = "exp_data/Freq{}_Policy{}".format(args.freq, args.policy)
    # create dir in int and output data if not exists
    if not os.path.exists(exp_dir_name):
        os.makedirs(exp_dir_name)
    # experiment name
    exp_name = "{}/PB{}_SB{}_HB{}".format(exp_dir_name, 
                                    args.position_budget, 
                                    args.speed_budget, 
                                    args.heading_budget)
    # create dir if not exist
    if not os.path.exists(exp_name):
        os.makedirs(exp_name)

    logging.basicConfig(filename="{}/run.log".format(exp_name), format=FORMAT, level=basic_level, datefmt='%d/%m/%y %H:%M:%S:%m')
    logging.disable(logging.ERROR if args.quiet else logging.NOTSET)
    os.environ["TQDM_DISABLE"] = str(int(args.quiet))

    noise = diff.NoiseMachine(args.position_budget, args.speed_budget, args.heading_budget)
   
    main(args.directory, args.freq, args.policy, args.dimensions, 
         noise, exp_name)
    


