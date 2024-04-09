#! /bin/bash
PC_SCHEME=$1
declare -A PCS=( [1]="Periodical" [2]="Disposable" [3]="Distance" [4]="Random" [5]="Car2Car")
job_log_file () {
    echo "job_log/FQ${1}_PC${2}_PB-pos${3}_PB-speed${4}_PB-heading${5}"
}
rm -rf job_log
rm -rf exp_data
mkdir -p job_log
mkdir -p exp_data
for freq in {1..1}
do
    for budget in `seq 0 0.01 0.1`
    do
        # Position Only
        RUN_FILE=$(job_log_file $freq $PC_SCHEME $budget 0 0)
        echo $RUN_FILE
        python scripts/tracker.py -dir data/ -fq $freq -pc $PC_SCHEME -pb $budget >> $RUN_FILE.log 2>&1

        # Speed Only
        RUN_FILE=$(job_log_file $freq $PC_SCHEME 0 $budget 0)
        echo $RUN_FILE
        python scripts/tracker.py -dir data/ -fq $freq -pc $PC_SCHEME -sb $budget >> $RUN_FILE.log 2>&1

        # Heading Only
        RUN_FILE=$(job_log_file $freq $PC_SCHEME 0 0 $budget)
        echo $RUN_FILE
        python scripts/tracker.py -dir data/ -fq $freq -pc $PC_SCHEME -hb $budget >> $RUN_FILE.log 2>&1

        # Speed + Position + Heading
        RUN_FILE=$(job_log_file $freq $PC_SCHEME $budget $budget $budget)
        echo $RUN_FILE
        python scripts/tracker.py -dir data/ -fq $freq -pc $PC_SCHEME -hb $budget -sb $budget -pb $budget >> $RUN_FILE.log 2>&1
    done
done