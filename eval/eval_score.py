# -*- coding:utf-8 -*-
from __future__ import print_function
import codecs
import numpy as np
import math
import heapq
import random

negNum = 50


def get_hit_ratio(rank_list, target_item):
    for item in rank_list:
        if item == target_item:
            return 1
    return 0


def get_ndcg(rank_list, target_item):
    for i, item in enumerate(rank_list):
        if item == target_item:
            return math.log(2) / math.log(i + 2)
    return 0


def eval_one_rating(i_gnd, i_pre, K):
    if sum(i_pre) == 0:
        return 0, 0
    map_score = {}
    for item, score in enumerate(i_pre):
        map_score[item] = score

    target_item = i_gnd.index(1.0)

    rank_list = heapq.nlargest(K, map_score, key=map_score.get)
    hit = get_hit_ratio(rank_list, target_item)
    ndcg = get_ndcg(rank_list, target_item)
    return hit, ndcg


if __name__ == "__main__":
    # read pos user ids
    user_id_list = []
    user_id_reader = codecs.open("user_id.txt", mode="r", encoding="utf-8")
    for line in user_id_reader:
        user_id_list.append(line.strip())
    user_id_reader.close()

    # generate test samples
    pos_reader = codecs.open("total_pos_sorted.txt", mode="r", encoding="utf-8")
    neg_reader = codecs.open("total_neg_sorted.txt", mode="r", encoding="utf-8")
    pos_line = pos_reader.readline()
    neg_line = neg_reader.readline()

    debug_num = 0
    hit_k_score = []
    ndcg_k_score = []
    for user_id in user_id_list:
        print("user id:", user_id)

        user_pos_list = []
        # read positive items
        while pos_line:
            pos_line_list = pos_line.strip().split("\t")
            if pos_line_list[0] == user_id:
                user_pos_list.append(pos_line_list)
                pos_line = pos_reader.readline()
            else:
                # pos_line = pos_reader.readline()
                break

        user_neg_list = []
        # read negative items
        while neg_line:
            neg_line_list = neg_line.strip().split("\t")
            if neg_line_list[0] == user_id:
                user_neg_list.append(neg_line_list)
                neg_line = neg_reader.readline()
            else:
                # neg_line = neg_reader.readline()
                break

        # samples
        for pos_item in user_pos_list:
            if len(user_neg_list) > negNum:
                neg_sample_list = random.sample(user_neg_list, negNum)
            else:
                neg_sample_list = user_neg_list
            ground_truth_labels = []
            predict_labels = []
            ground_truth_labels.append(float(pos_item[-2]))
            predict_labels.append(float(pos_item[-1]))
            for _item in neg_sample_list:
                ground_truth_labels.append(float(_item[-2]))
                predict_labels.append(float(_item[-1]))

            _hit, _ndcg = eval_one_rating(i_gnd=ground_truth_labels, i_pre=predict_labels, K=15)
            hit_k_score.append(_hit)
            ndcg_k_score.append(_ndcg)

    pos_reader.close()
    neg_reader.close()

    print("hit@15", sum(hit_k_score)/len(hit_k_score))
    print("ndcg@15", sum(ndcg_k_score)/len(ndcg_k_score))