#!/usr/bin/env bash
echo "test part 1"
python format_entity_pair.py "test.list"

for i in {1..13}
do
    echo $i
    python format_entity_pair.py "test_"$i".list"
done