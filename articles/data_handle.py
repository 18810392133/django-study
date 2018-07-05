#!/user/bin/env python
#-*- coding:utf8 -*-
#@TIME   :2018/6/27 7:58
#@Author :weige
#@File :data_handle.py


import numpy as np
import pandas as pd
from sklearn import model_selection as cv
from sklearn.metrics.pairwise import pairwise_distances
from articles import user_behavior as user_behavior

def predict(ratings, similarity, type='user'):
    if type == 'user':
        # axis =1 ：压缩列，对各行求均值，返回 m *1 矩阵
        mean_user_rating = ratings.mean(axis=1)
#         print(mean_user_rating)
        ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
        pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array(
            [np.abs(similarity).sum(axis=1)]).T
    elif type == 'item':
        pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])#dot()两矩阵相乘，abs()取绝对值
    return pred
# 接受user_id  输出recommend id list
def recommend(user_id):
    article_id_list = [i for i in range(33,103)]
    # 你要处理的是哪一行
    index_line_tosort = user_behavior.user_id_list.index(user_id)
    #从整理好的list之中选出最大的五个
    sorted_user_prediction_line = sorted(user_prediction[index_line_tosort])
    # print(len(sorted_user_prediction_line))
    top_five = []
    a = len(sorted_user_prediction_line)
    while(len(top_five)<5):
        top_five.append(sorted_user_prediction_line[a-1])
        a-=1
    # print(top_five)
    # 拿到每个top的索引   这个就是article_id_list的索引
    top_five_article_index = []
    for i in range(len(top_five)):
        top_five_article_index.append(user_prediction[index_line_tosort].index(top_five[i]))
    top_five_article_id = []
    for i in range(len(top_five_article_index)):
        index = top_five_article_index[i]
        top_five_article_id.append(article_id_list[index])
    # print(top_five_article_id)
    return top_five_article_id


    # 1、读取u.data(csv格式)中的数据
header = ['user_id', 'item_id', 'rating','x','y']
df = pd.read_csv(r'E:\workspace\Pycharmworkspace\laoqi_django_book\articles\read_counts_divide10.csv', names=header,index_col=False)
# print(df[:10])

 # 2、统计有多少个不重复的user以及多少个不重复的产品
n_users = df.user_id.unique().shape[0]
n_items = df.item_id.unique().shape[0]
# print ('Number of users = ' + str(n_users) + ' | Number of items = ' + str(n_items))

 # 4、构建两个user-item矩阵，一个是给训练数据集，一个是给测试数据集
train_data_matrix = np.zeros((n_users, n_items))
for line in df.itertuples():
#         print(line)
        train_data_matrix[int(line[4]), int(line[5])] = line[3]
# print(train_data_matrix[3])

# 5、利用sklearn的pairwise_distances函数来计算余弦相似性，生成user相似性矩阵和item相似性矩阵
user_similarity = pairwise_distances(train_data_matrix, metric='cosine')
item_similarity = pairwise_distances(train_data_matrix.T, metric='cosine')
# print(user_similarity.shape)
# print(user_similarity)
# print(item_similarity.shape)
# print(item_similarity)

# 6、利用相似性矩阵做推荐
user_prediction = predict(train_data_matrix, user_similarity, type='user')
item_prediction = predict(train_data_matrix, item_similarity, type='item')
user_prediction = user_prediction-2
user_prediction = user_prediction.tolist()
# print(user_prediction[0])
# for i in range(19,33):
    # print(i)
    # print(recommend(i))
