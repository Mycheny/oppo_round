import time

import pandas as pd
import numpy as np
from pandas import DataFrame


def test_feature(data):
    a = data.groupby(['label']).size().reset_index()
    print(a)
    b = data[data.duplicated()].count()
    print(b)
    # 得到Series中的唯一值数值
    prefix = data['prefix'].unique()
    query_prediction = data['query_prediction'].unique()
    title = data['title'].unique()
    tag = data['tag'].unique()
    label = data['label'].unique()
    # 计算一个Series中各值出现的频率
    prefix = data['prefix'].value_counts()
    query_prediction = data['query_prediction'].value_counts()
    title = data['title'].value_counts()
    tag = data['tag'].value_counts()
    label = data['label'].value_counts()
    # 判断成员资格
    prefix = data[data['prefix'].isin(["重庆旅游"])]
    qp = '{"重庆旅游景区": "0.018", "重庆旅游攻略": "0.373", "重庆旅游景点大全": "0.020", "重庆旅游职业学院": "0.038", "重庆旅游景点": "0.215", "重庆旅游地图": "0.013", "重庆旅游景点排名前十": "0.016", "重庆旅游必去的地方": "0.005", "重庆旅游攻略三日游": "0.027", "重庆旅游攻略景点必去": "0.015"}'
    query_prediction = data[data['query_prediction'].isin([qp])]
    title = data[data['title'].isin(["皇包车旅行"])]
    tag = data[data['tag'].isin(["应用"])]
    label = data[data['label'].isin(["1"])]
    # 生产统计
    d = data.describe()
    return data


def get_feature(data):
    feature = pd.DataFrame(data, columns =["prefix","title","tag"])
    prefixs = data['prefix'].value_counts()

    print("########## tag 点击率 ###########")
    tag_hits ={}
    tags = data['tag'].value_counts()
    for index, tag in zip(tags.index, tags):
        a = data[data['label'].isin(["1"]) & data['tag'].isin([index])].values
        tag_hits[index] = a.shape[0]/tag
        print(index, a.shape[0]/tag)
    feature["tag"] = feature['tag'].replace(tag_hits)

    print("########## prefix 点击率 ###########")
    prefix_hits = {}
    prefixs = data['prefix'].value_counts()
    for index, prefix in zip(prefixs.index, prefixs):
        a = data[data['label'].isin(["1"]) & data['title'].isin([index])].values
        prefix_hits[index] = a.shape[0]/prefix
    feature["prefix"] = feature['prefix'].replace(prefix_hits)

    print("########## title 点击率 ###########")
    title_hits = {}
    titles = data['title'].value_counts()
    for index, title in zip(titles.index, titles):
        a = data[data['label'].isin(["1"]) & data['title'].isin([index])].values
        title_hits[index] = a.shape[0] / title
    feature["title"] = feature['title'].replace(title_hits)
    print()

if __name__ == '__main__':
    train = "C:\\tmp\自动驾驶\\oppo_round\\oppo_round1_train_20180929\\oppo_round1_train_20180929.txt"
    vali = "C:\\tmp\自动驾驶\\oppo_round\\oppo_round1_vali_20180929\\oppo_round1_vali_20180929.txt"
    test = "C:\\tmp\自动驾驶\\oppo_round\\oppo_round1_test_20180929\\oppo_round1_test_20180929.txt"

    with open(vali, encoding="utf-8") as f:
        lines = f.readlines()
        lines = [line.replace("\n", "").split("\t") for line in lines]
    data = DataFrame(lines)
    data.columns = ['prefix', 'query_prediction', 'title', 'tag', 'label']
    feature = get_feature(data)
    print()
