#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "MambaHJ"

import os
import pandas as pd

def get_data(data_name=''):
	current_path = os.getcwd()
	parent_dir = os.path.dirname(current_path)
	print(parent_dir)
	for f in os.listdir(parent_dir):
		print(f)
		if f.endswith("data"):
			data_path = os.path.join(parent_dir, f)
	for f in os.listdir(data_path):
		if f.endswith(data_name):
			data_path = os.path.join(data_path, f)
	data = pd.read_excel(data_path, index_col=u'日期')
	return data,os.path.join(current_path,'/')

def check_plot(data,command="",show_flag=False):
	import matplotlib.pyplot as plt
	if show_flag:
		if command == "plotdata":
			data.plot()
			plt.xlabel('date')
			plt.ylabel('sales')
			plt.legend('s')
			plt.savefig('timeseries.png')
			plt.show()
		elif command == "acf":
			from statsmodels.graphics.tsaplots import plot_acf
			plot_acf(data)
			plt.savefig('acf.png')
			plt.show()
		elif command == "pacf":
			from statsmodels.graphics.tsaplots import plot_pacf
			plot_pacf(data)
			plt.savefig('pacf.png')
			plt.show()
		elif command == "boxplot":
			fig = plt.figure()
			p = data.boxplot(return_type='dict')
			x = p['fliers'][0].get_xdata()
			y = p['fliers'][0].get_ydata()
			y.sort()	
			# xy 为被注释的坐标点
			# xytext 为注释文字的坐标位置
			for i in range(len(x)):
				if i > 0:
					plt.annotate(y[i], xy=(x[i], y[i]), xytext=(x[i]+0.05-0.8/(y[i]-y[i-1]), y[i]))
				else:
					plt.annotate(y[i], xy=(x[i], y[i]), xytext=(x[i]+0.08, y[i]))
			plt.savefig('box.png')
			plt.show()

def check_adf(data):
	from statsmodels.tsa.stattools import adfuller as ADF
	print(u"原始序列的单位根检验结果：{}".format(ADF(data[u'销量'])))

def check_noise(data):
	# 白噪声检验
	from statsmodels.stats.diagnostic import acorr_ljungbox
	# 返回统计量和p值
	print(u"白噪声检验结果为：{}".format(acorr_ljungbox(data, lags=1)))


if __name__ == '__main__':
	data,root_path = get_data(data_name='catering_sale.xls')
	print("根目录：{}\n初始数据概览：\n{}".format(root_path,data.describe()))
	# 绘制箱线图，剔除异常值
	check_plot(data=data,command='boxplot',show_flag=True)
	# 根据打印的箱线图，选取[400,6000]的数据
	data = data[(data[u'销量']>400)&(data[u'销量']<6000)]

	print("剔除异常值后数据概览：\n{}".format(data.describe()))
	check_plot(data=data,command='plotdata',show_flag=True)
	check_plot(data=data,command='acf',show_flag=True)
	check_adf(data)
	# p值<0.05，可以拒绝原假设，不存在单位根，为平稳序列，下一步进行白噪声检验
	check_noise(data=data)
	# p值<0.05, 可以拒绝原序列是一个白噪声序列的假设, 下一步，模型定阶
	check_plot(data=data,command='pacf',show_flag=True)
	# 这里不太方便模块化，直接写了
	from statsmodels.tsa.arima_model import ARMA
	data[u'销量'] = data[u'销量'].astype(float)
	pmax = int(len(data)/10)
	qmax = int(len(data)/10)
	bic_mat = []
	for p in range(pmax+1):
		tmp = []
		for q in range(qmax+1):
	 		try:
	 			tmp.append(ARMA(data,(p,q)).fit().bic)
	 		except:
	 			tmp.append(None)
		bic_mat.append(tmp)
	bic_mat = pd.DataFrame(bic_mat)
	p,q = bic_mat.stack().idxmin()
	# print(bic_mat)
	print(u"bic最小的p值和q值分别为：{}，{}".format(p, q))
	model = ARMA(data,(1,0)).fit()
	print(model.summary2())
	print(model.forecast(5))


