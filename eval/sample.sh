#!/usr/bin/env bash
alpha_array=("0.2" "0.4" "0.6" "0.8" "1.0")
for alpha in ${alpha_array[@]}
do
  echo "sample on "alpha
  python sample.py $alpha "pos_items.txt" "neg_items.txt"
done