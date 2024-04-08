#! /bin/bash
declare -A PCS=( [1]="Periodical" [2]="Disposable" [3]="Distance" [4]="Random" [5]="Car2Car")
job_log_file () {
    return "job_log/FQ${1}_PC${2}_PB-pos${3}_PB-speed${4}_PB-heading${5}"
}
for fq in {1..1}
do
    for pc in {1..1}
    do  
        for budget in `seq 0 0.0025 0.1`
        do
            # Position Only
            RUN_FILE=$(job_log_file $fq $pc $budget 0 0)
            echo $RUN_FILE
            python scripts/tracker.py -dir data/ -fq $fq -pc $pc -pb $budget >> $RUN_FILE.log 2>&1

            # Speed Only
            RUN_FILE=$(job_log_file $fq $pc 0 $budget 0)
            echo $RUN_FILE
            python scripts/tracker.py -dir data/ -fq $fq -pc $pc -sb $budget >> $RUN_FILE.log 2>&1

            # Heading Only
            RUN_FILE=$(job_log_file $fq $pc 0 0 $budget)
            echo $RUN_FILE
            python scripts/tracker.py -dir data/ -fq $fq -pc $pc -hb $budget >> $RUN_FILE.log 2>&1

            # Speed + Position + Heading
            RUN_FILE=$(job_log_file $fq $pc $budget $budget $budget)
            echo $RUN_FILE
            python scripts/tracker.py -dir data/ -fq $fq -pc $pc -hb $budget -sb $budget -pb $budget >> $RUN_FILE.log 2>&1
        done
    done
done
