#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "MambaHJ"

import numpy as np

# 线性回归
# 最小二乘法
from sklearn.linear_model import LinearRegression
reg_model = LinearRegression()
x = np.mat([[0,0],[1,1],[2,2]])
y = np.mat([[0],[1],[2]])
reg_model.fit(x,y)
print('自变量系数：{} 截距：{}'.format(reg_model.coef_,reg_model.intercept_))

# 岭回归避免多重共线问题
from sklearn.linear_model import Ridge
x_1 = np.mat([[0,0],[0,0],[1,1]])
y_1 = np.mat([[0],[.1],[1]])
reg_model = Ridge(alpha = .5,fit_intercept=True)
reg_model.fit(x_1,y_1)
print('自变量系数：{} 截距：{}'.format(reg_model.coef_,reg_model.intercept_))
# 通过内置的 Alpha 参数的交叉验证来实现岭回归
from sklearn.linear_model import RidgeCV
x_2 = np.mat([[0,0],[0,0],[1,1]])
y_2 = np.mat([[0],[.1],[1]])
reg_model = RidgeCV(alphas=[0.1,1.0,10.0],fit_intercept=True)
reg_model.fit(x_2,y_2)
print('自变量系数：{} 截距：{}'.format(reg_model.coef_,reg_model.intercept_))
print('最适参数alpha：{}'.format(reg_model.alpha_))
print('x1=1,x2=2时，函数值为：{}'.format(reg_model.predict([[1,1]])))
print('拟合函数的得分：{}'.format(reg_model.score(x_2,y_2)))
# 多项式回归
from sklearn.preprocessing import PolynomialFeatures
x = np.arange(6).reshape(3,2)
print('x: \n{}'.format(x))
# 把x转化为最高项为2次的多项式形式
poly = PolynomialFeatures(degree=2)
x = poly.fit_transform(x)
print('转变之后x:\n{}'.format(x))
# 通过Pipeline工具来简化
from sklearn.pipeline import Pipeline
model = Pipeline([('poly',PolynomialFeatures(degree=3)),
	('linear',LinearRegression(fit_intercept=False))])
x_1 = np.arange(5)
y = 3 - 2*x_1 + x_1**2 - x_1**3
model = model.fit(x_1[:,np.newaxis],y)
print('多项式回归系数：{}'.format(model.named_steps['linear'].coef_))




