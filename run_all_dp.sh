#! /bin/bash

eval "$(conda shell.bash hook)"
conda activate uda

set -eu

declare -A PCS=( [1]="Periodical" [2]="Disposable" [3]="Distance" [4]="Random" [5]="Car2Car")


for fq in {1..1}
do
    for pc in {1..1}
    do  
        for hb in `seq 0 0.0025 0.1`
        do
            echo -e "Executing the PTF with frequency $fq and policy $pc -> \"${PCS[$pc]}\" hb -> $hb" 
            # run the next command twice in parallel
            RUN_FILE="job_log/FQ${fq}_PC${pc}_HB${hb}"
            echo $RUN_FILE
            python tracker.py -dir data/ -fq $fq -pc $pc -hb $hb >> $RUN_FILE.log 2>&1
        done
    done
done