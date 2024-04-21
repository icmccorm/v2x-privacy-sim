
POSITIONAL_INCREMENT=$1
ARBITRARY_INCREMENT=$2
for STEP in $(seq 0 1 50)
do
    POSITIONAL_BUDGET=$(echo "$STEP * $POSITIONAL_INCREMENT" | bc)
    ARBITRARY_BUDGET=$(echo "$STEP * $ARBITRARY_INCREMENT" | bc)
    for PRIVACY_MODE in $(seq 1 1 4)
    do
        for CHANGE_SCHEME in {1..5}
        do
            printf "%s\\n%s\\n%s\\n%s\\n" "$CHANGE_SCHEME" "$POSITIONAL_BUDGET" "$ARBITRARY_BUDGET" "$PRIVACY_MODE" "1"
        done
    done
done