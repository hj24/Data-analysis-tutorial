# Chapter 1 数据质量的分析

S1. 箱线图分析

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

  