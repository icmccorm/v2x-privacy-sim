# Evaluating Differential Privacy for Location Data in V2X Communication

This GitHub repository contains our extension to the pseudonym tracking simulation used in [Zoccoli et al.'s paper](https://ieeexplore.ieee.org/document/10333561): "Are VANETs pseudonyms effective? An experimental evaluation of pseudonym tracking in adversarial scenario". Their original repository is available [here](https://github.com/GGZ8/PTF/tree/7156d10d2da4e3e8568d7a3b56551804281c4e7d). We modified their simulation to apply differential privacy to the heading, speed, and location of vehicles using [bounded laplacian noise](https://programming-dp.com/ch5.html) and [geo-indistinguishability](https://arxiv.org/pdf/1212.1984) methods. 

# Setup
We used Python [3.9.9](https://www.python.org/downloads/release/python-399/), and our dependencies are specified in the provided [requirements.txt](https://github.com/icmccorm/v2x-privacy-sim/blob/main/requirements.txt) file. 
```bash
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```
After configuring a virtual environment, to test the framework, you will need to download the output from Zoccoli et al.'s simulation, which is a compressed archive named [simulation_output.tgz](https://github.com/GGZ8/PTF/blob/7156d10d2da4e3e8568d7a3b56551804281c4e7d/simulation_output.tgz). Decompress the archive and ensure that its output `data` directory is present in the root folder of the repository. 
```bash
wget https://github.com/SECloudUNIMORE/ACS/raw/master/PTS/simulation_output.tgz
tar xzf simulation_output.tgz
```    
Alternatively, you can build our Docker image, which performs each of the previous steps automatically. Equivalent instructions are also present in the README for the [original repository](https://github.com/GGZ8/PTF/tree/7156d10d2da4e3e8568d7a3b56551804281c4e7d). 

# Execution
You can execute a single iteration of the simulation using the following command:
```bash
python3 tracker.py -dir data/ -fq 1 -pc 1 -pb 0.1 -sb 0.1 -hb 0.1
```
Or alternatively, use `make test`. 

The following configuration options are available:
```
| Option  | Desc                                            |
|---------|-------------------------------------------------|
| -h      | Show the help message                           |
| -q      | Disable logging                                 |
| -d      | Enable debug logging                            |
| -fq [f] | Specify the frequency. Only '1' is supported    |
| -pc [p] | Specify the pseudonym change policy. (1-5)      |
| -dim    | Consider dimensions when linking.               |
| -pb [b] | Specify the privacy budget for position (>= 0). |
| -sb [b] | Specify the privacy budget for speed (>=0).     |
| -hb [b] | Specify the privacy budget for heading (>=0).   |
```
The following pseudonym change policies are supported:
```
| ID | Name       |
|----|------------|
| 1  | Periodical |
| 2  | Disposable |
| 3  | Distance   |
| 4  | Random     |
| 5  | Car2Car    |
```
Refer to the [original paper](https://ieeexplore.ieee.org/document/10333561) for detailed descriptions of each policy.

# Data Collection
We conducted a large-scale evaluation of multiple combinations of pseudonym change policies and privacy budgets for speed, position, and heading. To recreate our results, you can execute the following command:
```
./scripts/eval/run_all_dp_in_parallel.sh 0.8 0.004 0.3
```

The first argument is the minimum value for the position budget. The second is the increment for the position budget and the third is the increment for the speed and heading budgets, which begin at 0. This difference is due to the clipping mechanim we use for positional noise, which Zoccoli et al. describe in section 4.3. This will execute 100 iterations of the simulation for each pseudonym change scheme and combination of differential privacy mechanisms at each of the increments. 

Or alternatively, `make eval-dp`. This command launches up to 6 processes to run the simulation multiple times in parallel. This will create a folder `exp_data` with the following files:
```
- exp_data
    |- results.csv
    |- results_compiled.csv
    |- err.log                  
```
The file `err.log` will contain all text written to `stderr` throughout the simulation. It should be empty after a successful run. The file `results.csv` contains the results of each execution. Every row is a single execution, with the following columns:
```
| Column                   | Desc                    |
|--------------------------|-------------------------|
| speed_budget             | Speed privacy budget    |
| position_budget          | Position privacy budget |
| adjusted_position_budget | See Zoccoli et al. 4.3  |
| fq                       | Frequency               |
| pc                       | Pseudonym change scheme |
| prec                     | Precision               |
| recall                   | Recall                  |
| f1_score                 | F1 Score                |
| dpt_mean                 | Mean change in position |
| dpt_max                  | Max change in position  |
```
The file `results_compiled.csv` has equivalent contents, but they are lengthened to indicate whether noise is being applied to only one attribute or to each of speed, heading, and position. Noise values are also normalized as `budget_step` increments from 0 to 100, with zero indicating the minimum noise value and 100 indicating the maximum. 

The results we use in our final report are provided in [results.zip](). 