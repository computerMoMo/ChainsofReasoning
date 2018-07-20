#!/usr/bin/env bash
mode_path=$1
result_path=$2
echo"model testing..."
bash model_test.sh $mode_path "0" $result_path
bash combine_result.sh $result_path
bash concat.sh $result_path
python resort.py $result_path"/total_combine.txt" $result_path"/total_combine_sorted.txt"
bash eval_socre.sh $result_path"/total_combine_sorted.txt" $result_path

