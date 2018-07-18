# -*- coding:utf-8 -*-
from __future__ import print_function
import codecs
import numpy as np
import math
import heapq
import random
import sys
import os

negNum = 100


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

    alpha = float(sys.argv[1])
    print("eval with alpha:", alpha)

    not_enough_num = 0

    # generate test samples
    pos_reader = codecs.open(sys.argv[2], mode="r", encoding="utf-8")
    neg_reader = codecs.open(sys.argv[3], mode="r", encoding="utf-8")
    sample_reader = codecs.open("test_samples/test_samples_"+str(alpha)+".txt", mode="r", encoding="utf-8")

    pos_line = pos_reader.readline()
    neg_line = neg_reader.readline()
    sample_line = sample_reader.readline()

    debug_num = 0
    hit_k_score = []
    ndcg_k_score = []
    for user_id in user_id_list:
        print("user id:", user_id)
        user_item_pos_dict = dict()
        # read positive items
        while pos_line:
            pos_line_list = pos_line.strip().split("\t")
            if pos_line_list[0] == user_id:
                pos_line = pos_reader.readline()
                user_item_pos_dict[(pos_line_list[0], pos_line_list[1])] = (1.0, pos_line_list[-1])
            else:
                break

        # read negative items
        user_item_neg_dict = dict()
        while neg_line:
            neg_line_list = neg_line.strip().split("\t")
            if neg_line_list[0] == user_id:
                neg_line = neg_reader.readline()
                user_item_neg_dict[(neg_line_list[0], neg_line_list[1])] = (0.0, neg_line_list[-1])
            else:
                break

        print("user item pos len:", len(user_item_pos_dict), "user item neg len:", len(user_item_neg_dict))

        test_sample_list = []
        # read test samples
        while sample_line:
            sample_line_list = sample_line.strip().split("\t")
            if sample_line_list[0] == user_id:
                test_sample_list.append(sample_line_list)
                sample_line = sample_reader.readline()
            else:
                break

        # samples
        for test_object in test_sample_list:
            pos_pair = (user_id, test_object[1])
            neg_pair_list = []
            for neg_idx in test_object[2].split("#"):
                neg_pair_list.append((user_id, neg_idx))

            ground_truth_labels = []
            predict_labels = []
            print("pairs", pos_pair, user_item_pos_dict[pos_pair])
            ground_truth_labels.append(1.0)
            predict_labels.append(float(user_item_pos_dict[pos_pair][1]))

            for neg_pair in neg_pair_list:
                _scores = user_item_neg_dict[neg_pair]
                ground_truth_labels.append(0.0)
                predict_labels.append(float(_scores[1]))

            _hit, _ndcg = eval_one_rating(i_gnd=ground_truth_labels, i_pre=predict_labels, K=15)
            temp_hit = []
            temp_ndcg = []
            for k in range(1, 16):
                hit, ndcg = eval_one_rating(i_gnd=ground_truth_labels, i_pre=predict_labels, K=k)
                temp_hit.append(hit)
                temp_ndcg.append(ndcg)

            hit_k_score.append(temp_hit)
            ndcg_k_score.append(temp_ndcg)

    pos_reader.close()
    neg_reader.close()

    total_hit_res_array = np.asarray(hit_k_score)
    total_ndcg_res_array = np.asarray(ndcg_k_score)
    print(total_hit_res_array.shape)
    print(total_ndcg_res_array.shape)

    hit_average = []
    ndcg_average = []
    for i in range(15):
        hit_average.append("%.5f" % np.mean(total_hit_res_array[:, i]))
        ndcg_average.append("%.5f" % np.mean(total_ndcg_res_array[:, i]))
    print("hit score:", hit_average)
    print("ndcg score:", ndcg_average)

    score_dir = sys.argv[4]
    score_writer = codecs.open(os.path.join(score_dir, "eval_res_%.1f.txt" % alpha), mode="w", encoding="utf-8")
    score_writer.write("hit scores\t:" + "\t".join(hit_average) + "\n")
    score_writer.write("ndcg scores\t:" + "\t".join(ndcg_average) + "\n")
    score_writer.close()
