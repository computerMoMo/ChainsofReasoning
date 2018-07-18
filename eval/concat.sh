#!/usr/bin/env bash
echo "cat file"
pos_file_list_str="test_combine.txt "
for i in {1..13}
do
    pos_file_list_str=$pos_file_list_str" test_"$i"_combine.txt"
done
cat $pos_file_list_str > "total_combine.txt"

#echo "cat negative file"
#neg_file_list_str="test_neg.txt "
#for i in {1..13}
#do
#    neg_file_list_str=$neg_file_list_str" test_"$i"_neg.txt"
#done
#cat $neg_file_list_str > "total_neg.txt"
