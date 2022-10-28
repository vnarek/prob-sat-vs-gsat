#!/bin/bash
touch res.csv

tries=(300 400 500);
flips=(20 50 100 120);

for max_tries in ${tries[@]}; do
	for max_flips in ${flips[@]}; do
		for f in $(find dataset/ -type f | shuf -n 10); do
			for ((j=1; j < 15; j++)); do
				echo "running $max_tries $max_flips $f $j"
				out="$(python3 main.py -i $max_flips -T $max_tries $f 2>&1 >/dev/null)"
				echo $out $f prob_sat $max_tries $max_flips >> res.csv

				out="$(./gsat -r time -i $max_flips -T $max_tries $f 2>&1 >/dev/null)"
				echo $out $f gsat $max_tries $max_flips >> res.csv
			done
		done
	done
done