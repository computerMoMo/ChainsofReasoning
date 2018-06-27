# -*- coding:utf-8 -*-
from __future__ import print_function
import codecs

if __name__ == "__main__":
    pos_user_id_list = []
    pos_reader = codecs.open("total_pos.txt", mode="r", encoding="utf-8")
    line = pos_reader.readline()
    while line:
        line_list = line.strip().split("\t")
        pos_user_id_list.append(int(line_list[0]))
        line = pos_reader.readline()
    pos_reader.close()

    pos_user_id_list = set(pos_user_id_list)
    print(len(pos_user_id_list))

    pos_user_id_list = sorted(list(pos_user_id_list))
    user_id_writer = codecs.open("user_id.txt", mode="w", encoding="utf-8")
    for user_id in pos_user_id_list:
        user_id_writer.write(str(user_id)+"\n")
    user_id_writer.close()
