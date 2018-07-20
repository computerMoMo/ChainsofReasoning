#!/usr/bin/env bash
model_path=$1
gpu_id=$2
result_path=$3

echo "part 1 test"
bash model_test_one_list.sh $1 $result_path'/test.res' $2 'test.list'

for i in {1..13}
do
    echo $i
    bash model_test_one_list.sh $1 $result_path'/test_'$i'.res' $2 'test_'$i'.list'
done