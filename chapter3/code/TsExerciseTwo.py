#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "MambaHJ"

import pandas as pd
import numpy as np
import os

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
	print(u"序列的单位根检验结果：{}".format(ADF(data)))

def check_noise(data):
	# 白噪声检验
	from statsmodels.stats.diagnostic import acorr_ljungbox
	# 返回统计量和p值
	print(u"白噪声检验结果为：{}".format(acorr_ljungbox(data, lags=1)))

def main():
	current_path = os.getcwd()
	parent_path = os.path.dirname(current_path)
	assert 'data' in os.listdir(parent_path)
	data_path = os.path.join(parent_path,'data')
	for f in os.listdir(data_path):
		if f.endswith('xlsx'):
			data_path = os.path.join(data_path,f)
	print("数据路径: {}".format(data_path))
	print("读取第一个sheet的数据：")
	data = pd.read_excel(data_path,
						skiprows=[0],
						index_col=u'指标名称',
						sheet_name=0)
	# 打印数据概况
	describe = data.describe()
	print(describe)
	# 取均值来填充缺失值
	for i in range(10,15):
		data.iloc[31,i] = data.iloc[:30,i].mean()
		
	init_data = data.iloc[:32,10:15].astype(float)
	print(init_data.iloc[:,0])
	# 从时序图和自相关图可以看出是非平稳序列
	check_plot(init_data.iloc[:,0],command='plotdata',show_flag=False)
	check_plot(init_data.iloc[:,0],command='acf',show_flag=False)
	# 单位根存在，进一步验证
	check_adf(init_data.iloc[:,0])
	# 进行差分运算
	D_data = init_data.iloc[:,0].diff().dropna()
	D_data.columns = [u'指标差分']
	check_plot(D_data,command='plotdata',show_flag=True)
	check_adf(D_data)	#1阶差分后得平稳序列
	check_plot(D_data,command='acf',show_flag=True)
	check_plot(D_data,command='pacf',show_flag=True)
	# 白噪声检验
	check_noise(D_data)

	# 白噪声检验结果为：(array([ 1.93646543]), array([ 0.16405283]))
	# 没有建模的必要了
	
if __name__ == '__main__':
	main()