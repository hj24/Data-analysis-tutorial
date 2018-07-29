#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pandas as pd

__author__ = "MambaHJ"

current_path = os.getcwd()
dir_name = os.path.dirname(current_path)
catering_sale = dir_name + '/data/catering_sale.xls'
# 读取数据，指定日期列为索引
data = pd.read_excel(catering_sale, index_col = u'日期')
# 数据文件的大概描述，包括均值，数量，最大值等等
statistics = data.describe()
print("数据概况：\n {}".format(statistics))
# loc是根据dataframe的具体标签选取列，而iloc是根据标签所在的位置，从0开始计数
count = statistics.loc['count'][0]
std = statistics.loc['std'][0]
print("count: {} std: {}".format(count, std))
# 在文件的基础属性上衍生计算出来的其他值，如极差，变异系数
# data.describe()可以通过loc直接添加标签
# 极差
statistics.loc['range'] = statistics.loc['max'][0] - statistics.loc['min'][0]
# 变异系数
statistics.loc['cv'] = statistics.loc['std'][0] / statistics.loc['mean'][0]
print("修改后：\n {} \nsize: {}".format(statistics, len(data)))

import matplotlib.pyplot as plt
# 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 用来正常显示负号
plt.rcParams['axes.unicode_minus'] = False

plt.figure()
# DataFrame里画箱线图的方法
p = data.boxplot(return_type = 'dict')
x = p['fliers'][0].get_xdata()
y = p['fliers'][0].get_ydata()
y.sort()

# 设置标签
for i in range(len(x)):
    if i > 0:
        plt.annotate(y[i], xy=(x[i], y[i]), xytext=(x[i]+0.05-0.8/(y[i]-y[i-1]), y[i]))
    else:
        plt.annotate(y[i], xy=(x[i], y[i]), xytext=(x[i]+0.08, y[i]))

plt.show()
# 根据箱线图剔除异常值
data = data[(data[u'销量'] > 400)&(data[u'销量'] < 6000)]
print("剔除异常值后:\t", len(data))