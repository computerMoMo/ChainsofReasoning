#!/usr/bin/env bash
for i in {1..13}
do
    echo $i
    python combine_result.py "test_"$i".list.entity" 'test_'$i'.res' 'test_'$i
done