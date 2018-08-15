# Chapter 1 数据质量的分析

## S1. 箱线图分析

1. 箱线图分析是异常值分析中的一种常用方法

2. 该方法标准是：异常值通常被定义为小于QL - 1.5IQR或大于Qu + 1.5IQR的值，

   - 其中QL称为下四分位数，表示全部观察值中有四分之一的数据取值比它小
   - Qu称为上四分位数，表示全部观察值中有四分之一的数据取值比它大
   - IQR则是四分位间距，是Qu与QL之差，包含全部观察值一般

   ![](https://ws4.sinaimg.cn/large/006tKfTcgy1ftmiw2xuf9j306q0770tc.jpg)

3. 箱线图依据实际数据绘制，直观反映数据分布的本来面貌，而且它的判断标准四分位数有一定鲁棒性：多达25%的数据可以变得任意远而不会很大扰动四分位数，所以一般而言，异常值不能对这个标准施加影响

4. 具体问题实例：

- 实例代码所分析的数据中可能会产生异常值，如图，少部分数据过小：

  ![](https://ws1.sinaimg.cn/large/006tKfTcgy1ftmixwkshvj305406t74h.jpg)

- 数据集见`chapter1/data/catering_sale.xls`,代码见`chapter1/code/OutlierAanlysis.py`

- 代码分析：

  1. 首先导入所需要的模块，pandas，os等，然后是一些固定格式，不多解释了：

  ```python
  #!/usr/bin/env python
  # -*- coding: utf-8 -*-
  import os
  import pandas as pd
  # 下面这一行只是一个标志，说明代码是我写的，可以忽略...
  __author__ = "MambaHJ"
  ```

  2. 读取数据并初步打印一下数据的概况

     ```python
     #得到当前目录的位置本例中也就是code这个目录
     current_path = os.getcwd()
     # 根据当前目录得到父级目录
     dir_name = os.path.dirname(current_path)
     catering_sale = dir_name + '/data/catering_sale.xls'
     # 按日期这一列为索引值读取数据
     data = pa.read_excel(catering_sale, index_col=u'日期')
     # 读取数据的大致情况，包括均值最大值等
     statistics = data.describe()
     print("数据概况：\n {}".format(statistics))
     """
     loc是根据标签取列，iloc是根据位置索引值取列
     下面是从statistcs取出相关有用信息的代码
     """
     count = statistics.loc['count'][0]
     std = statistics.loc['std'][0]
     print("count: {} std: {}".format(count, std))
     ```

     运行结果：

     ![](https://ws3.sinaimg.cn/large/006tNc79gy1ftqj5sltoqj3086056aag.jpg)

  3. 根据基础属性计算所需要的其他值，如极差，变异系数等

     ```python
     """
     可以直接用loc添加标签
     """
     # 标准差
     statistics.loc['range'] = statistics.loc['max'][0] - statistics['min'][0]
     # 变异系数
     statistics.loc['cv'] = statistics.loc['std'][0] / statistics.loc['mean'][0]
     print("修改后：\n {} \nsize: {}".format(statistics, len(data)))
     ```

     运行结果：

     ![](https://ws4.sinaimg.cn/large/006tNc79gy1ftqjnlpg6mj306106bdg8.jpg)

  4. 可视化，绘制箱线图

     ```python
     import matplotlib.pyplot as plt
     """
     下面两行用来显示正常中文标签和符号
     然而在我的机器上并没有卵用...
     """
     plt.rcParams['font.sans-serif'] = ['SimHei']
     plt.rcParams['axes.unicode_minus'] = False
     
     plt.figure()
     # 调用DataFrame里画箱线图的方法
     p = data.boxplot(return_type='dict')
     # fliers为异常值的标签
     x = p['fliers'][0].get_xdata()
     y = p['fliers'][0].get_ydata()
     y.sort()	# 排序
     
     """
     用annotate添加注释，参数详解如下：
     
     第一个参数：是注释的内容
     xy：设置箭头的坐标
     xytext：设置注释的起始位置
     arrowprops：设置箭头形式
     facecolor：设置箭头的颜色
     headlength：箭头的头的长度
     headwidth：箭头的宽度
     width：箭身的宽度
     
     需要用以下代码控制一下注释重叠的部分
     以下代码只针对此题情况，其它状况需自行调整
     """
     
     for i in range(len(x)):
         if i>0:
             plt.annotate(y[i],xy=(x[i],y[i]),xytext=(x[i]+0.05-0.8/(y[i]-y[i-1]),y[i]))
         else:
             plt.annotate(y[i], xy=(x[i], y[i]), xytext=(x[i]+0.08, y[i]))
     # 展示箱线图
     plt.show()
     # 剔除异常值
     data = data[(data[u'销量']>400)&(data[u'销量']<6000)]
     print("剔除异常值之后：{}".format(len(data)))
     ```

     运行结果：

     ![](https://ws3.sinaimg.cn/large/006tNc79gy1ftqmh1ut69j304f0133yj.jpg)

     箱线图：

     ![](https://ws4.sinaimg.cn/large/006tNc79gy1ftqmh45vlzj30hs0dcaa8.jpg)