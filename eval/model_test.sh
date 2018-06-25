#!/bin/bash

data_dir='../data/movie_output_data'
predicate_name='rate'
mean_model=3
model_path=$1
out_file=$2

#this will output score file
th test_from_checkpoint_cpu.lua -input_dir $data_dir  -out_file $out_file -predicate_name $predicate_name -meanModel $mean_model -model_path $model_path