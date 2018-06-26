# -*- coding:utf-8 -*-
import codecs
import os
import sys

movie_data_dir = "movie_output_data/rate/"
pad_entity_id = "11463"

if __name__ == "__main__":
    test_list = []
    file_reader = codecs.open(os.path.join(movie_data_dir, sys.argv[1]), mode="r", encoding="utf-8")
    for line in file_reader.readlines():
        test_list.append(line.strip())
    file_reader.close()

    entity_pair_writer = codecs.open(os.path.join(movie_data_dir, sys.argv[1]+".entity"), mode="w", encoding="utf-8")
    # entity_pair_writer.write("label\tstart_entity_id\tend_entity_id\n")
    for file_name in test_list:
        int_reader = codecs.open(os.path.join(movie_data_dir, file_name.replace("torch", "int")), mode="r", encoding="utf-8")
        line = int_reader.readline()
        while line:
            line_list = line.strip().split("\t")
            label = line_list[0]
            path_list = line_list[1].split(";")
            one_path = path_list[0]

            start_entity_id = ""
            item_list = one_path.split(" ")
            for item in item_list:
                _temp_list = item.split(",")
                if _temp_list[1] != pad_entity_id:
                    start_entity_id = _temp_list[1]
                    break
            end_entity_id = item_list[-1].split(",")[1]

            # label start_entity_id end_entity_id
            entity_pair_writer.write(label+"\t"+start_entity_id+"\t"+end_entity_id+"\n")
            # read next line
            line = int_reader.readline()
        int_reader.close()
    entity_pair_writer.close()
