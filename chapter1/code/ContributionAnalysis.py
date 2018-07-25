#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import os
__author__ = "MambaHJ"

"""
帕累托法则，20/80定律

"""
current_path = os.getcwd()
dir_name = os.path.dirname(current_path)
dish_profit = dir_name + '/data/catering_dish_profit.xls'

data = pd.read_excel(dish_profit, index_col = u'菜品名')
print(data.describe())
profit = data[u'盈利'].copy()
# 原书接口改变，sort改为sort_values()
# ascending = False 时降序排列
profit.sort_values(ascending = False)
print(profit)

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.figure()
profit.plot(kind = 'bar')
plt.ylabel(u'profit(yuan)')
# cumsum()是累加求和
p = 1.0 * profit.cumsum() / profit.sum()
print(p)
p.plot(color = 'r', secondary_y = True, style = '-o', linewidth =2)
plt.annotate(format(p[6], '.4%'), xy = (6, p[6]), xytext = (6 * 0.9, p[6] * 0.9), arrowprops = dict(arrowstyle = "->", connectionstyle = "arc3, rad = 2"))
plt.ylabel(u'profit(proportion)')
plt.show()