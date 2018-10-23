import datetime
import csv

import numpy as np
import pandas as pd
import time
from math import *
import matplotlib.pyplot as plt

import xgboost as xgb
from matplotlib import pyplot
from xgboost import plot_importance

from bickRental.Comfort import Comfort


def mylog(data):
    data = int(data) + 1
    return log(data)


def get_feature(dataset):
    feature = pd.DataFrame()
    feature["hours"] = list(
        map(lambda d: mylog(int(d.hour)), dataset['datetime'].astype('datetime64')))  # 提取datetime 的小时作为特征
    feature['season'] = dataset['season']  # 季节
    feature['holiday'] = dataset['holiday']  # 是否假日
    feature['workingday'] = dataset['workingday']  # 是否工作日
    feature['weather'] = dataset['weather']  # 天气 越大天气越糟糕
    feature['temp'] = dataset['temp'].apply(func=mylog)  # 温度
    feature['atemp'] = dataset['atemp'].apply(func=mylog)  # 体感温度

    feature['feeling'] = dataset['atemp'] - dataset['temp']  # 实际温度和人的体感温度的差异
    feature['humidity'] = dataset['humidity'].apply(func=mylog)  # 湿度
    feature['windspeed'] = dataset['windspeed'].apply(func=mylog)  # 风速

    comfort = Comfort()
    fun = comfort.isPtInPoly_one
    l = np.array(dataset[['atemp', 'humidity', 'season']]).tolist()
    feature['comfort'] = list(map(fun, l))  # 计算当天的湿度和温度是否让人感到舒适

    return feature.values


if __name__ == '__main__':
    feature_train = pd.DataFrame()
    feature_test = pd.DataFrame()
    result = pd.DataFrame()
    label = pd.DataFrame()

    dataset = pd.read_csv('../data/train.csv', delimiter=",", skiprows=0)

    trainData = get_feature(dataset)
    label['count'] = dataset['count'].apply(func=mylog).values
    offset = 10800
    xgtrain = xgb.DMatrix(trainData[:offset, :], label=label[:offset])
    xgeval = xgb.DMatrix(trainData[offset:, :], label=label[offset:])

    watchlist = [(xgtrain, 'train'), (xgeval, 'val')]
    params = {"max_depth": 8, "tree_num": 1000, "silent": 1, "shrinkage": 0.1}
    # 训练模型
    # 训练结果在迭代到14次时在xgtrain和xgeval上表现最好,其平均方差分别是0.305665和0.358867
    model = xgb.train(list(params.items()), xgtrain, 450, watchlist, early_stopping_rounds=100)  # 训练结果在前10800
    # 绘制参数对结果的影响情况
    plot_importance(model)
    # pyplot.show()

    # 测试数据
    dataset = pd.read_csv('../data/test.csv', delimiter=",", skiprows=0)

    testData = get_feature(dataset)
    xgtest = xgb.DMatrix(testData)

    preds = model.predict(xgtest, ntree_limit=model.best_iteration).tolist()
    preds = [int(exp(i) - 1) for i in preds]

    result['datetime'] = dataset['datetime']
    result['count'] = preds

    result.to_csv('../data/result.csv', index=False)  # 预测结果保存为 result.csv 文件

    plt.figure()
    plt.plot(result['datetime'][24 * 18:24 * 22], result['count'][24 * 18:24 * 22])
    plt.xlabel("time(s)")
    plt.ylabel("count(m)")
    plt.savefig("../data/easyplot.jpg")
    plt.show()  # 显示图
