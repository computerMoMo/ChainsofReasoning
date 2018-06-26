#!/bin/bash

data_dir='../data/movie_output_data'
predicate_name='rate'
mean_model=3
model_path=$1
out_file=$2
gpu_id=$3
test_list_file=$4

#this will output score file
th test_from_checkpoint.lua -input_dir $data_dir  -out_file $out_file -predicate_name $predicate_name -meanModel \
    $mean_model -model_path $model_path -test_list $test_list_file -gpu_id $gpu_id