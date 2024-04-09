
for j in $(seq 0 $2 $1)
do
    for m in $(seq 1 1 4)
    do
        for i in {1..5}
        do
            printf "%s\\n%s\\n%s\\n%s\\n" "$i" "$j" "$m" "1"
        done
    done
done