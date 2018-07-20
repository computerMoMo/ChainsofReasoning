#!/usr/bin/env bash
result_path=$1
echo "test part 1"
python combine_result.py "test.list.entity" $result_path'/test.res' $result_path'/test'

for i in {1..13}
do
    echo $i
    python combine_result.py "test_"$i".list.entity" $result_path'/test_'$i'.res' $result_path'/test_'$i
done