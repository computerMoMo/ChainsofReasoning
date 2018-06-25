# -*- coding:utf-8 -*-
from __future__ import print_function
import codecs
import os
import sys

entity_dir = "../data/movie_output_data/rate"

if __name__ == "__main__":
    file_reader = codecs.open(sys.argv[1], mode="r", encoding="utf-8")
    item_list = []
    line = file_reader.readline()
    while line:
        line_list = line.strip().split("\t")
        item_list.append((int(line_list[0]), line_list[1], line_list[2], line_list[3]))
        line = file_reader.readline()
    file_reader.close()

    print("resort")
    resort_list = sorted(item_list, key=lambda x: x[0])
    print("sorted done!")
    file_writer = codecs.open(sys.argv[2], mode="w", encoding="utf-8")
    for item in resort_list:
        file_writer.write(str(item[0])+"\t"+item[1]+"\t"+str(item[2])+"\t"+item[3]+"\n")
    file_writer.close()
