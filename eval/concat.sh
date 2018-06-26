#!/usr/bin/env bash
echo "cat positive file"
pos_file_list_str="test_pos.txt "
for i in {1..13}
do
    pos_file_list_str=$pos_file_list_str" test_"$i"_pos.txt"
done
cat $pos_file_list_str > "total_pos.txt"

echo "cat negative file"
neg_file_list_str="test_neg.txt "
for i in {1..13}
do
    neg_file_list_str=$neg_file_list_str" test_"$i"_neg.txt"
done
cat $neg_file_list_str > "total_neg.txt"
