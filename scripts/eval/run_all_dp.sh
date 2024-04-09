#! /bin/bash
PC_SCHEME=$1
job_log_file () {
    RUN_FILE="$JOB_LOG_DIR/PB-pos${1}_PB-speed${2}_PB-heading${3}.log"
    if [ -f $RUN_FILE ]; then
        echo "Error: $RUN_FILE already exists"
        exit 1
    fi
    echo $RUN_FILE
}
mkdir -p job_log
mkdir -p exp_data
for freq in {1..1}
do  
    JOB_LOG_DIR="job_log/Freq${freq}_Policy${PC_SCHEME}"
    rm -rf $JOB_LOG_DIR
    mkdir -p $JOB_LOG_DIR
    for budget in `seq 0.01 0.01 0.1`
    do
        # Position Only
        job_log_file $budget 0.0 0.0
        python scripts/tracker.py -dir data/ -fq $freq -pc $PC_SCHEME -pb $budget >> $RUN_FILE 2>&1

        # Speed Only
        job_log_file 0.0 $budget 0.0
        python scripts/tracker.py -dir data/ -fq $freq -pc $PC_SCHEME -sb $budget >> $RUN_FILE 2>&1

        # Heading Only
        job_log_file 0.0 0.0 $budget
        python scripts/tracker.py -dir data/ -fq $freq -pc $PC_SCHEME -hb $budget >> $RUN_FILE 2>&1

        # Speed + Position + Heading
        job_log_file $budget $budget $budget
        python scripts/tracker.py -dir data/ -fq $freq -pc $PC_SCHEME -hb $budget -sb $budget -pb $budget >> $RUN_FILE 2>&1
    done
done