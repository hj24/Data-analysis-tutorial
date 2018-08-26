#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "MambaHJ"

import os 
import pandas as pd
from sklearn.decomposition import PCA
import numpy as np

def test_1():
	data = np.random.rand(10,4)
	print('数据概况：\n{}'.format(data))
	pca = PCA(n_components=2)
	pca.fit(data)
	print('特征向量：\n{}'.format(pca.components_))
	print('各属性贡献率：\n{}'.format(pca.explained_variance_ratio_))

def test_2():
	data = pd.read_excel('/Users/macbook/Desktop/Data-analysis-tutorial/chapter2/data/2018-51MCM-Appendix B.xlsx',
		index_col='指标名称',
		sheet_name=0,
		skiprows=[0])
	print('数据概况：\n{}'.format(data.describe()))
	data_train = data.iloc[:32,:20]
	
	for i in range(data_train.shape[0]):
		for j in range(data_train.shape[1]):
			if data_train.iloc[i,j] == '——':
				data_train.iloc[i,j] = np.nan
	data_train = data_train.fillna(axis=0,method='ffill')	
	print('填补缺失值后: \n{}'.format(data_train))
	pca = PCA(n_components=3)
	pca.fit(data_train.T)
	print('特征向量：\n{}'.format(pca.components_))
	print('各属性贡献率：\n{}'.format(pca.explained_variance_ratio_))
	
if __name__ == '__main__':
	choice = False
	if choice:
		test_1()
	else:
		test_2()