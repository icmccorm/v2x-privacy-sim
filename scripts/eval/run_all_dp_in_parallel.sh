#! /bin/bash
CURR_DIR=$(pwd)
printf %s\\n {1..5} | xargs -n 1 -P 5 $CURR_DIR/scripts/eval/run_all_dp.sh
