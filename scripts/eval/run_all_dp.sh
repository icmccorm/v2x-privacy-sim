#! /bin/bash
PC_SCHEME=$1
POSITIONAL_BUDGET=$2
ARBITRARY_BUDGET=$3
MODE=$4
FREQ=$5
declare PCS=( [1]="Periodical" [2]="Disposable" [3]="Distance" [4]="Random" [5]="Car2Car")
declare MODES=( [1]="Position" [2]="Speed" [3]="Heading" [4]="All")
echo -e "($POSITIONAL_BUDGET, $ARBITRARY_BUDGET, $FREQ, ${PCS[$PC_SCHEME]}, ${MODES[$MODE]})"
JOB_LOG_PARENT_DIR="exp_data/Freq${FREQ}_Policy${PC_SCHEME}"
mkdir -p $JOB_LOG_PARENT_DIR
ERR_LOG_FILE="exp_data/err.log"
touch $ERR_LOG_FILE
if [ $MODE -eq 1 ]; then
    python scripts/tracker.py -q -dir data/ -fq $FREQ -pc $PC_SCHEME -pb $POSITIONAL_BUDGET > /dev/null 2>> $ERR_LOG_FILE
elif [ $MODE -eq 2 ]; then
    python scripts/tracker.py -q -dir data/ -fq $FREQ -pc $PC_SCHEME -sb $ARBITRARY_BUDGET > /dev/null 2>>$ERR_LOG_FILE
elif [ $MODE -eq 3 ]; then
    python scripts/tracker.py -q -dir data/ -fq $FREQ -pc $PC_SCHEME -hb $ARBITRARY_BUDGET > /dev/null 2>>$ERR_LOG_FILE
elif [ $MODE -eq 4 ]; then
    python scripts/tracker.py -q -dir data/ -fq $FREQ -pc $PC_SCHEME -hb $ARBITRARY_BUDGET -sb $ARBITRARY_BUDGET -pb $POSITIONAL_BUDGET > /dev/null 2>>$ERR_LOG_FILE
fi