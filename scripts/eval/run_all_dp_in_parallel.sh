#! /bin/bash
CURR_DIR=$(pwd)
$CURR_DIR/scripts/eval/generate_jobs.sh 0.8 0.072 0.001 | xargs -n 5 -P 6 $CURR_DIR/scripts/eval/run_all_dp.sh
echo 'speed_budget,position_budget,adjusted_position_budget,heading_budget,fq,pc,prec,recall,f1_score,diff_pos_transformation' > exp_data/results.csv
find exp_data -name "run.csv" -exec sed -n '1p' {} \; >> exp_data/results.csv