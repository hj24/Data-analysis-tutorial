#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "MambaHJ"

import pandas as pd
import os

def get_data(data_name=''):
	current_path = os.getcwd()
	parent_path = os.path.dirname(current_path)
	data_dir = os.path.join(parent_path,'data')
	for f in os.listdir(data_dir):
		if f.endswith(data_name):
			data_path = os.path.join(data_dir,f)
	data = pd.read_excel(data_path,index_col='Id')
	return data,os.path.dirname(data_path)

def output_file(data,file_path=''):
	data_dir = os.path.join(file_path,'tmp')
	output = 'data_type.xls'
	output = os.path.join(data_dir,output)
	data.to_excel(output)

def density_plot(data,title):
	import matplotlib.pyplot as plt
	plt.figure()
	# 逐列作图
	for i in range(len(data.iloc[0])):
		(data.iloc[:,i]).plot(kind='kde',label=data.columns[i],linewidth=2)
	plt.ylabel(u'density')
	plt.xlabel(u'population')
	plt.title(u'cluster class {} density'.format(title))
	plt.legend()
	return plt

def density_plot(data,k):
	import matplotlib.pyplot as plt
	p = data.plot(kind='kde',linewidth=2,subplots=True,sharex=False)
	[p[i].set_ylabel(u'density') for i in range(k)]
	plt.legend()
	return plt

def tsne_plot(data_zs,r,show_flag=False):
	if show_flag:
		# 使用TSNE进行数据降纬并展示聚类结果
		from sklearn.manifold import TSNE
		tsne = TSNE()
		# 进行降维
		tsne.fit_transform(data_zs)
		# 转换数据格式
		tsne = pd.DataFrame(tsne.embedding_,index=data_zs.index)
		# 把不同类别用不同颜色和样式绘制
		print(tsne)
		import matplotlib.pyplot as plt
		d = tsne[r[u'聚类类别'] == 0]
		plt.plot(d[0],d[1],'r.')
		d = tsne[r[u'聚类类别'] == 1]
		plt.plot(d[0],d[1],'go')
		d = tsne[r[u'聚类类别'] == 2]
		plt.plot(d[0],d[1],'b*')
		plt.show()

def main():
	data, data_path= get_data(data_name='consumption_data.xls')
	print(u'打印数据：\n{}\n数据概况：\n{}'.format(data,data.describe()))
	# 聚类类别
	k = 3
	# 聚类最大循环次数
	iteration = 500
	# 数据标准化
	data_zs = 1.0*(data - data.mean())/data.std()
	print(u'标准化之后的数据：\n{}\n数据概况：\n{}'.format(data_zs,data_zs.describe()))
	from sklearn.cluster import KMeans
	# 分为k类，并发数为4
	model = KMeans(n_clusters=k,n_jobs=4,max_iter=iteration)
	# 开始聚类
	model.fit(data_zs)
	# 简单打印结果
	# 统计各个类别数目
	r_1 = pd.Series(model.labels_).value_counts()
	# 找出聚类中心
	r_2 = pd.DataFrame(model.cluster_centers_)
	# 横向连接(0 是纵向)，得到聚类中心对应类别下的数目
	r = pd.concat([r_2,r_1],axis=1)
	# 重命名表头
	r.columns = list(data.columns)+[u'类别数目']
	print(u'聚类概况：\n{}'.format(r))
	# 详细输出原始数据及其类别
	r = pd.concat([data,pd.Series(model.labels_,index=data.index)],axis=1)
	r.columns = list(data.columns)+[u'聚类类别']
	print(u'聚类详情：\n{}'.format(r))
	# 将聚类结果保存
	output_file(r,file_path=os.path.dirname(data_path))
	pic_output = os.path.join(os.path.dirname(data_path),'tmp/pd_')
	# for i in range(k):
	# 	density_plot(data[r[u'聚类类别'] == i],k=k).savefig(u'{}{}.png'.format(pic_output,i))
	# 使用TSNE进行数据降纬并展示聚类结果
	tsne_plot(data_zs,r=r,show_flag=True)

if __name__ == '__main__':
	main()