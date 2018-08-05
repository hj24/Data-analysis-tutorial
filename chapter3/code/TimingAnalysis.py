#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "MambaHJ"

import pandas as pd
import os

current_dir = os.getcwd()
root_dir = os.path.dirname(current_dir)
data_path = os.path.join(root_dir, "data/arima_data.xls")
data = pd.read_excel(data_path, index_col=u'日期')

import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# 绘制时序图
data.plot()
plt.legend("sales")
plt.xlabel("date")
plt.ylabel("sales")

# 绘制自相关图
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# plot_acf(data)
# plt.show()
# 单位根检验
from statsmodels.tsa.stattools import adfuller as ADF
print(u"原始序列的单位根检验结果：{}".format(ADF(data[u'销量'])))
# 返回值依次是adf, pvalues, usedlag, nobs, critical values, icbest, regresults, resstore

# 对非平稳序列建模首先要进行差分运算，把它差分成平稳序列
# 差分后的结果
D_data = data.diff().dropna()
D_data.columns = [u'销量差分']
D_data.plot()	# 时序图
plt.ylabel("diff_sales")
plt.legend("diff_sales")
plot_acf(D_data)	# 自相关图
plot_pacf(D_data)	# 偏自相关图
plt.show()
print(u"差分序列的单位根检验结果：{}".format(ADF(D_data[u'销量差分'])))

# 白噪声检验
from statsmodels.stats.diagnostic import acorr_ljungbox
# 返回统计量和p值
print(u"差分序列的白噪声检验结果为：{}".format(acorr_ljungbox(D_data, lags=1)))

from statsmodels.tsa.arima_model import ARIMA
# 模型定阶
data[u'销量'] = data[u'销量'].astype(float) 	# 注意训练时序模型时要传进去的是float型
pmax = int(len(D_data)/10)		# 一般阶数不超过长度的十分之一
qmax = int(len(D_data)/10)
bic_mat = []
for p in range(pmax+1):
	tmp = []
	for q in range(qmax+1):
		try: #	拟合原序列
			# 人为观察出来用MA(1)模型拟合差分序列，即对1阶差分后的原数据进行ARIMA(p,1,q)模型
			tmp.append(ARIMA(data, (p,1,q)).fit().bic)
		except:
			tmp.append(None)
	bic_mat.append(tmp)

bic_mat = pd.DataFrame(bic_mat)
print(bic_mat)
p,q = bic_mat.stack().idxmin()
print(u"bic最小的p值和q值为：{}，{}".format(p,q))
# 建立ARIMA（0，1，1）模型
model = ARIMA(data, (p,1,q)).fit()
print(model.summary2())
# 作为期5天的预测，返回预测结果，标准误差，置信区间
print(model.forecast(5))
