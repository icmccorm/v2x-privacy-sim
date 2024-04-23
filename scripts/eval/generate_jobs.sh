
POSITIONAL_START=$1
POSITIONAL_INCREMENT=$2
ARBITRARY_INCREMENT=$3
touch jobs.csv
for STEP in $(seq 0 1 100)
do
    POSITIONAL_BUDGET=$(echo "scale=3; $STEP * $POSITIONAL_INCREMENT + $POSITIONAL_START" | bc)
    ARBITRARY_BUDGET=$(echo "scale=3; $STEP * $ARBITRARY_INCREMENT" | bc)
    for PRIVACY_MODE in $(seq 1 1 4)
    do
        for CHANGE_SCHEME in {1..5}
        do
            printf "%s\\n%s\\n%s\\n%s\\n" "$CHANGE_SCHEME" "$POSITIONAL_BUDGET" "$ARBITRARY_BUDGET" "$PRIVACY_MODE" "1"
        done
    done
done