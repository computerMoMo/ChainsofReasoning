# -*- coding:utf-8 -*-
from __future__ import print_function
import codecs
import numpy as np
import math
import heapq
import random
import sys

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


def generate_fq_dict(alpha, origin_fq_dict):
    sum_pros = 0.0
    for item_id, item_fq in origin_fq_dict.items():
        sum_pros += item_fq**alpha

    new_item_fq_dict = dict()
    for item_id, item_fq in origin_fq_dict.items():
        new_item_fq_dict[item_id] = item_fq**alpha/sum_pros
    return new_item_fq_dict


def sample_with_fq(sample_num, item_fq_list):
    sample_id_list = []
    while True:
        temp_res = list(np.random.multinomial(sample_num * 5, item_fq_list, 1)[0])
        if temp_res.count(0) <= len(item_fq_list) - sample_num:
            for idx, res in enumerate(temp_res):
                if res > 0:
                    sample_id_list.append((idx, res))
            sample_id_list = sorted(sample_id_list, key=lambda x: x[1], reverse=True)
            return [item[0] for item in sample_id_list[:100]]


if __name__ == "__main__":
    # read pos user ids
    user_id_list = []
    user_id_reader = codecs.open("user_id.txt", mode="r", encoding="utf-8")
    for line in user_id_reader:
        user_id_list.append(line.strip())
    user_id_reader.close()

    # read origin fq dict
    item_fq_reader = codecs.open("../data/movie_vocab/path_rnn_movie_fq.txt", mode="r", encoding="utf-8")
    item_fq_dict = dict()
    for line in item_fq_reader.readlines():
        line_list = line.strip().split("\t")
        item_fq_dict[line_list[0]] = float(line_list[1])
    item_fq_reader.close()

    alpha = float(sys.argv[1])

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
                if alpha == 0.0:
                    neg_sample_list = random.sample(user_neg_list, negNum)
                else:
                    print("generate new item sample pros with alpha:", alpha)
                    itemFqDict = generate_fq_dict(alpha=alpha, origin_fq_dict=item_fq_dict)
                    item_fq_list = [itemFqDict[item_id] for item_id in user_neg_list]
                    neg_sample_list = sample_with_fq(sample_num=negNum, item_fq_list=item_fq_list)
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
            temp_hit = []
            temp_ndcg = []
            for k in range(1, 16):
                hit, ndcg = eval_one_rating(i_gnd=ground_truth_labels, i_pre=predict_labels, K=k)
                temp_hit.append(hit)
                temp_ndcg.append(ndcg)

            hit_k_score.append(temp_hit)
            ndcg_k_score.append(temp_ndcg)

            # print(_hit, _ndcg)
            # hit_k_score.append(_hit)
            # ndcg_k_score.append(_ndcg)
        # debug
        # debug_num += 1
        # if debug_num >= 10:
        #     break

    pos_reader.close()
    neg_reader.close()

    # print("hit@15", sum(hit_k_score)/float(len(hit_k_score)))
    # # print(sum(hit_k_score), len(hit_k_score))
    # print("ndcg@15", sum(ndcg_k_score)/float(len(ndcg_k_score)))

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

    score_writer = codecs.open("eval_res_%.1f.txt" % alpha, mode="w", encoding="utf-8")
    score_writer.write("\t".join(hit_average) + "\n")
    score_writer.write("\t".join(ndcg_average) + "\n")
    score_writer.close()