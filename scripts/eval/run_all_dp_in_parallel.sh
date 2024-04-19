#! /bin/bash
CURR_DIR=$(pwd)
$CURR_DIR/scripts/eval/generate_jobs.sh 0.1 0.0025 | xargs -n 4 -P 6 $CURR_DIR/scripts/eval/run_all_dp.sh
echo 'position_budget,speed_budget,heading_budget,fq,pc,prec,recall,f1_score' > exp_data/results.csv
find exp_data -name "run.csv" -exec sed -n '1p' {} \; >> exp_data/results.csv