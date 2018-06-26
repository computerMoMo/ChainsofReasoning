#!/usr/bin/env bash
model_path=$1
gpu_id=$2

for i in {1..13}
do
    echo $i
    bash model_test.sh $1 'test_'$i'.res' $2 'test_'$i'.list'
done