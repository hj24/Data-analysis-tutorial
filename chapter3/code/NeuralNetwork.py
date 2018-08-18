#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "MambaHJ"

import pandas as pd
import numpy as np
import os

def get_data(data_name='',index_col=''):
	current_path = os.getcwd()
	parent_path = os.path.dirname(current_path)
	data_dir = os.path.join(parent_path,'data')
	for f in os.listdir(data_dir):
		if f.endswith(data_name):
			data_path = os.path.join(data_dir,f)
	data = pd.read_excel(data_path,index_col=index_col)
	return data,os.path.dirname(data_path)

def cm_plot(y, yp):
  from sklearn.metrics import confusion_matrix 
  cm = confusion_matrix(y, yp) 
  
  import matplotlib.pyplot as plt 
  plt.matshow(cm, cmap=plt.cm.Greens) 
  plt.colorbar() 
  
  for x in range(len(cm)): 
    for y in range(len(cm)):
      plt.annotate(cm[x,y], xy=(x, y), horizontalalignment='center', verticalalignment='center')
  
  plt.ylabel('True label') 
  plt.xlabel('Predicted label') 
  return plt


if __name__ == '__main__':
	data,data_path = get_data('sales_data.xls', index_col=u'序号')
	print(u'数据概况: \n{}\n地址： {}'.format(data,data_path))
	# 用1表示‘好，是，高’ 0，表示’坏，否，低‘
	data[data == u'好'] = 1
	data[data == u'是'] = 1
	data[data == u'高'] = 1
	data[data != 1] = 0
	x = data.iloc[:,:3].as_matrix().astype(int)
	y = data.iloc[:,3].as_matrix().astype(int)
	print(u'数据概况: \n{}'.format(data))

	from keras.models import Sequential
	from keras.layers.core import Dense, Activation

	model = Sequential()
	model.add(Dense(10,input_shape=(3,)))
	model.add(Activation('relu'))
	model.add(Dense(1,input_shape=(10,)))
	model.add(Activation('sigmoid'))
	model.compile(loss='binary_crossentropy',optimizer='adam')
	model.fit(x,y,epochs=1000,batch_size=10)
	y_pred = model.predict_classes(x).reshape(len(y))
	pred = model.predict(x).reshape(len(y))
	
	y_predict = pd.Series(y_pred)
	y_probability = pd.Series(pred)
	y_mat = pd.concat([y_predict,y_probability],axis=1)
	y_mat.columns = ['预测值','预测概率']
	print(y_mat)
	cm_plot(y,y_predict).show()
	