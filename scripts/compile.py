import pandas as pd
import os
import sys
# take three arguments
if len(sys.argv) != 4:
    print("Usage: python compile.py <base_positional> <step_positional> <step_arbitrary>")
    sys.exit(1)

base_positional = float(sys.argv[1])
step_positional = float(sys.argv[2])
step_arbitrary = float(sys.argv[3])

results = pd.read_csv(os.path.join("./exp_data", "results.csv"))
results = results.drop(columns=['adjusted_position_budget'])

results['position_budget'] = round((results['position_budget'] - base_positional) / step_positional, 0)
results['speed_budget'] = round(results['speed_budget'] / step_arbitrary, 0)
results['heading_budget'] = round(results['heading_budget'] / step_arbitrary, 0)

speed = results[(results['heading_budget'] == 0) & (results['position_budget'] <= 0)].copy()
speed = speed.drop(columns=['heading_budget', 'position_budget'])
speed['mode'] = "speed"
speed = speed.rename(columns={'speed_budget': 'budget_step'}).drop_duplicates()

heading = results[(results['speed_budget'] == 0) & (results['position_budget'] <= 0)].copy()
heading = heading.drop(columns=['speed_budget', 'position_budget'])
heading['mode'] = "heading"
heading = heading.rename(columns={'heading_budget': 'budget_step'}).drop_duplicates()

position = results[(results['speed_budget'] == 0) & (results['heading_budget'] == 0) & (results['position_budget'] >= 0)].copy()
position = position.drop(columns=['speed_budget', 'heading_budget'])
position['mode'] = "position"
position = position.rename(columns={'position_budget': 'budget_step'}).drop_duplicates()

all = results[(results['position_budget'] >= 0) & (results['position_budget'] == results['speed_budget']) & (results['speed_budget'] == results['heading_budget'])].copy()
all = all.drop(columns=['speed_budget', 'heading_budget'])
all['mode'] = "all"
all = all.rename(columns={'position_budget': 'budget_step'}).drop_duplicates()

results_all = pd.concat([speed, heading, position, all])
results_all['budget_step'] = results_all['budget_step'].astype(int)
results_all['mode'] = results_all['mode'].apply(lambda x: x.title())
pcs = {1: "Periodical", 2: "Disposable", 3: "Distance", 4: "Random", 5: "Car2Car"}
results_all['pc'] = results_all['pc'].apply(lambda x: pcs[x])
results_all.iloc[:, 1:-1] = results_all.iloc[:, 1:-1].round(3)
results_all.to_csv(os.path.join('./exp_data', 'results_compiled.csv'), index=False)