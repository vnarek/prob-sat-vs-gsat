#!/bin/bash
touch res.csv

for f in uf20-91R/*; do
    for ((j=1; j < 100; j++)); do
        out="$(python3 main.py -i 5 $f 2>&1 >/dev/null)"
        echo $out $f prob_sat >> res.csv

        out="$(./gsat -r time -i 5 -T 300 $f 2>&1 >/dev/null)"
        echo $out $f gsat >> res.csv
    done
done