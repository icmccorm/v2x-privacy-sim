#! /bin/bash
printf %s\\n {1..5} | xargs -n 1 -P 5 -- /usr/src/v2x/scripts/eval/run_all_dp.sh {}