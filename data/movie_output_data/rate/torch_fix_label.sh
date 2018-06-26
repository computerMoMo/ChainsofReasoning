#!/usr/bin/env bash
data_set=("train" "test_part_2" "test")
for set in "${data_set[@]}"
do
    for torch_file in $set/*.torch
    do
        echo $torch_file
        th torch_fix_label.lua -input $torch_file
    done
done