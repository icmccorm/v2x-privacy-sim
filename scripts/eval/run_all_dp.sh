#! /bin/bash
PC_SCHEME=$1
DP_VALUE=$2
MODE=$3
FREQ=$4
declare PCS=( [1]="Periodical" [2]="Disposable" [3]="Distance" [4]="Random" [5]="Car2Car")
declare MODES=( [1]="Position" [2]="Speed" [3]="Heading" [4]="All")
echo -e "($DP_VALUE, $FREQ, ${PCS[$PC_SCHEME]}, ${MODES[$MODE]})"
JOB_LOG_PARENT_DIR="exp_data/Freq${FREQ}_Policy${PC_SCHEME}"
mkdir -p $JOB_LOG_PARENT_DIR
ERR_LOG_FILE="exp_data/err.log"
touch $ERR_LOG_FILE
if [ $MODE -eq 1 ]; then
    python scripts/tracker.py -q -dir data/ -fq $FREQ -pc $PC_SCHEME -pb $DP_VALUE > /dev/null 2>> $ERR_LOG_FILE
elif [ $MODE -eq 2 ]; then
    python scripts/tracker.py -q -dir data/ -fq $FREQ -pc $PC_SCHEME -sb $DP_VALUE > /dev/null 2>>$ERR_LOG_FILE
elif [ $MODE -eq 3 ]; then
    python scripts/tracker.py -q -dir data/ -fq $FREQ -pc $PC_SCHEME -hb $DP_VALUE > /dev/null 2>>$ERR_LOG_FILE
elif [ $MODE -eq 4 ]; then
    python scripts/tracker.py -q -dir data/ -fq $FREQ -pc $PC_SCHEME -hb $DP_VALUE -sb $DP_VALUE -pb $DP_VALUE > /dev/null 2>>$ERR_LOG_FILE
fi