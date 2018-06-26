#!/usr/bin/env bash
for i in {1..13}
do
    echo $i
    python format_entity_pair.py "test_"$i".list"
done