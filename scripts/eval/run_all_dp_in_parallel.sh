#! /bin/bash
CURR_DIR=$(pwd)
$CURR_DIR/scripts/eval/generate_jobs.sh 0.1 0.0025 | xargs -n 4 -P 6 $CURR_DIR/scripts/eval/run_all_dp.sh
