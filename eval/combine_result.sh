#!/usr/bin/env bash
echo "test part 1"
python combine_result.py "test.list.entity" 'test.res' 'test'

for i in {1..13}
do
    echo $i
    python combine_result.py "test_"$i".list.entity" 'test_'$i'.res' 'test_'$i
done