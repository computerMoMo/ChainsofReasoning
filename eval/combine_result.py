# -*- coding:utf-8 -*-
from __future__ import print_function
import codecs
import os
import sys

entity_dir = "../data/movie_output_data/rate"

if __name__ == "__main__":
    entity_reader = codecs.open(os.path.join(entity_dir, sys.argv[1]), mode="r", encoding="utf-8")
    # head_line = entity_reader.readline()
    result_reader = codecs.open(sys.argv[2], mode="r", encoding="utf-8")
    pos_combine_writer = codecs.open(sys.argv[3]+"_pos.txt", mode="w", encoding="utf-8")
    neg_combine_writer = codecs.open(sys.argv[3] + "_neg.txt", mode="w", encoding="utf-8")

    count_num = 0
    entity_line = entity_reader.readline()
    result_line = result_reader.readline()
    while entity_line and result_line:
        entity_list = entity_line.strip().split("\t")
        result_list = result_line.strip().split("\t")
        if result_list[-1] == "0":
            neg_combine_writer.write(entity_list[1]+"\t"+entity_list[2]+"\t"+result_list[-1]+"\t"+result_list[-2]+"\n")
        else:
            pos_combine_writer.write(entity_list[1]+"\t"+entity_list[2]+"\t"+result_list[-1]+"\t"+result_list[-2]+"\n")

        count_num += 1
        if count_num % 10000 == 0:
            print(count_num)
        # read next line
        entity_line = entity_reader.readline()
        result_line = result_reader.readline()
    entity_reader.close()
    result_reader.close()
    pos_combine_writer.close()
    neg_combine_writer.close()