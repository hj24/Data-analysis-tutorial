#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "MambaHJ"

import os 
import pandas as pd

def get_data(data_name='',index_col=''):
	current_path = os.getcwd()
	parent_path = os.path.dirname(current_path)
	data_dir = os.path.join(parent_path,'data')
	for f in os.listdir(data_dir):
		if f.endswith(data_name):
			data_path = os.path.join(data_dir,f)
	if index_col == '':
		data = pd.read_excel(data_path)
	else:
		data = pd.read_excel(data_path,index_col=index_col)
	return data,os.path.dirname(data_path)


if __name__ == '__main__':
	data,data_path = get_data('bankloan.xls',index_col='')
	x = data.iloc[:,:8].as_matrix()
	y = data.iloc[:,8].as_matrix()

	from sklearn.linear_model import LogisticRegression as LR
	from sklearn.linear_model import RandomizedLogisticRegression as RLR
	# 建立随机逻辑回归模型
	rlr = RLR()
	rlr.fit(x,y)
	print('获取特征筛选结果，也可以用.score_来获取：\n{}'.format(rlr.get_support()))
	print('通过随机逻辑回归模型筛选特征结束, 有效特征为：')
	for item in data.columns[:8][rlr.get_support()]:
		print('{}'.format(item))
	x = data[data.columns[:8][rlr.get_support()]].as_matrix()
	lr = LR()
	lr.fit(x,y)
	print('逻辑回训练结束')
	print('模型的平均正确率为：{}'.format(lr.score(x,y)))
	# 可以用lr.predict()来进进行预测

