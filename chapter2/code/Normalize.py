#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "MambaHJ"


import pandas as pd
import numpy as np
import os

def get_data_path(data_name=''):
	current_path = os.getcwd()
	parent_path = os.path.dirname(current_path)
	data_dir = os.path.join(parent_path,'data')
	for f in os.listdir(data_dir):
		if f.endswith(data_name):
			data_path = os.path.join(data_dir,f)
	return data_path

if __name__ == '__main__':
	data_path = get_data_path('normalization_data.xls')
	print(data_path)
	data = pd.read_excel(data_path,header=None)
	print('数据概况：\n{}'.format(data))
	# 离差标准化
	data_min_max = (data - data.min())/(data.max())
	print('经离差标准化后数据概况：\n{}'.format(data_min_max))
	# 标准差标准化
	data_std = (data - data.mean())/(data.std())
	print('经标准差标准化后数据概况：\n{}'.format(data_std))
	# 小数定标法
	data_float = data / (10**np.ceil(np.log10(data.abs().max())))
	print('经小数定标标准化后数据概况：\n{}'.format(data_float))