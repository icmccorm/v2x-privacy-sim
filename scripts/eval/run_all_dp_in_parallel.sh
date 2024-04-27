#! /bin/bash
CURR_DIR=$(pwd)
$CURR_DIR/scripts/eval/generate_jobs.sh $1 $2 $3 | xargs -n 5 -P 6 $CURR_DIR/scripts/eval/run_all_dp.sh
echo 'speed_budget,position_budget,adjusted_position_budget,heading_budget,fq,pc,prec,recall,f1_score,dpt_mean,dpt_max' > exp_data/results.csv
find exp_data -name "run.csv" -exec sed -n '1p' {} \; >> exp_data/results.csv
python3 ./scripts/compile.py $1 $2 $3
find exp_data -mindepth 1 -type d -exec rm -r {} \;