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
    combine_writer = codecs.open(sys.argv[3]+"_combine.txt", mode="w", encoding="utf-8")

    count_num = 0
    entity_line = entity_reader.readline()
    result_line = result_reader.readline()
    while entity_line and result_line:
        entity_list = entity_line.strip().split("\t")
        result_list = result_line.strip().split("\t")
        if int(result_list[-1]) != int(entity_list[0]):
            print(entity_line, result_line)
            break
        combine_writer.write(entity_list[1]+"\t"+entity_list[2]+"\t"+entity_list[0]+"\t"+result_list[-2]+"\n")
        count_num += 1
        if count_num % 10000 == 0:
            print(count_num)
        # read next line
        entity_line = entity_reader.readline()
        result_line = result_reader.readline()
    entity_reader.close()
    result_reader.close()
    combine_writer.close()
