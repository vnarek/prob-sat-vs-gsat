#!/bin/bash

rm -rf dataset/ || true

mkdir dataset/
dirs=(uf75-325 uf50-200 uf20-91R)

for d in ${dirs[@]}; do
	for file in $(find $d -type f | shuf -n 30); do
		cp $file dataset/
	done;
done
