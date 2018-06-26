# -*- coding:utf-8 -*-
from __future__ import print_function
import codecs
import os

data_dir = "movie_output_data/rate"

if __name__ == "__main__":
    # read
    file_reader = codecs.open("large_test_file.txt", mode="r", encoding="utf-8")
    large_list = []
    for line in file_reader.readlines():
        large_list.append(line.strip())
    file_reader.close()

    # split
    for file_name in large_list:
        print(file_name)
        file_writer_dict = dict()
        pre_str = file_name.replace("int", "part")
        for i in range(10):
            file_writer_dict[i] = codecs.open(os.path.join(data_dir, "test_part_2/"+pre_str+"_"+str(i)+".int"), mode="w", encoding="utf-8")
        int_file_reader = codecs.open(os.path.join(data_dir, "test/"+file_name), mode="r", encoding="utf-8")
        line = int_file_reader.readline()
        count_num = 0
        while line:
            writer_idx = count_num % 10
            file_writer_dict[writer_idx].write(line)
            count_num += 1
            line = int_file_reader.readline()
        int_file_reader.close()

        for i in range(10):
            file_writer_dict[i].close()
        path_count_num = file_name.split(".")[-2]
        list_writer = codecs.open(os.path.join(data_dir, "test_"+path_count_num+".list"), mode="w", encoding="utf-8")
        for i in range(10):
            list_writer.write("test_part_2/"+pre_str+"_"+str(i)+".torch\n")
        list_writer.close()