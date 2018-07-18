#!/usr/bin/env bash
alpha_array=("0.0" "0.2" "0.4" "0.6" "0.8" "1.0")
for alpha in ${alpha_array[@]}
do
  echo "evaluate on "alpha
  python temp_scores.py $alpha $1 $2 $3
done
