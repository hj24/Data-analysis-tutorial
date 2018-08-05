# Chapter 3 挖掘建模

##S1.时序模型

###简介

- 时间序列：就是按时间顺序排列的一组随机变量来表示一个随机事件。时间序列分析的目的就是给定一个已经被观测了的时间序列，预测该序列的未来值。在数学建模中这是必须掌握的技能。
- 在拿到数据进行分析时，经常会有预测数据走势这样的需求，因此，如何根据历史数据来预测未来数据就显得很重要了，这也是这一篇要着重总结的地方，以书上举得例子来看：
  - 就餐饮行业而言，生产和销售是同时进行的，因此销售预测对于餐饮企业十分必要，因为，根据菜品历史销售数据做好预测，可以有效减少菜品脱销现象和避免备料不足而导致的生产延误。
  - 同时，优秀的预测可以减少安全库存量，做到生产准时控制，降低物流成本。
  - 对餐饮销售的预测可以看做是基于时间序列的短板其数据预测，预测对象为具体菜品销售量。

### 时间序列算法

1. 常用算法

![](https://ws2.sinaimg.cn/large/006tNc79gy1ftwc5hvwc3j30lf0gw45r.jpg)

- 按参考书的安排，这里着重总结一下AR模型，MA模型，ARMA模型，ARIMA模型

2. 时间序列的预处理

   - 大致过程

     拿到一个观察值序列之后，我们不能确定这是不是一个含有有用信息的序列，如果这只是一个没有意义的序列，我们直接套用模型得出来的结果也是没有意义的是错误的，那么在后续的分析中只会一错再错，所以对一个序列，要想保证有用的分析，首先要对它进行随机性和平稳性的检验。

     根据上述两个检验结果，我们可以把序列分为不同的类型，对不同类型采取不同的分析方法。

   - 分析原则

     1. 对于纯随机序列，又称白噪声序列，序列的各项没有任何相关关系，只是在进行完全无序的随机波动

        这样的序列也就是上面我们所说的没有任何有用信息的序列，可以终止对该序列的分析。

     2. 对于平稳非白噪声序列，它的特点是均值和方差是常数，现已有一套非常成熟的平稳序列的建模方法。通常是建立一个线性模型(一般是ARMA模型)来拟合该序列。

     3. 对于非平稳非白噪声序列，均值和方差不稳定，我们通常把它转化为平稳序列，再用针对平稳序列的那套建模方法来分析。如果一个序列经过差分运算之后具有平稳性，则该序列为差分平稳序列，可以用ARIMA模型来进行分析。

   - 关于两个检验的介绍：

     1. 平稳性检验

        (1) 什么是平稳时间序列？

        - 这里我们有必要回顾一下协方差和相关系数的概念，对于一个随机变量，我们可以计算它的数学期望和方差，而对于两个(分别命名为X, Y)我们则可以计算他们的协方差和相关系数：	

        ![](https://ws4.sinaimg.cn/large/006tNc79gy1ftwjvq38iyg307i00k0sh.gif) 

        ![](https://ws2.sinaimg.cn/large/006tNc79gy1ftwjz1oj4gg304r0190pv.gif)

        ​	这两者度量了两个不同事件间的相互影响程度。

        - 回顾完上面两个概念之后，我们在回到事件序列上来，一个时间序列中的每一个序列值都是一个随机变量Xt，相应的它也有自己的均值和方差，但不同序列值并不是不同事件，那么要搞清楚它们之间的关系也就是同一时间在不同时期的相关程度，就要引入自协方差和自相关系数这两个概念。

        - 对于时间序列，在两不同时刻t, s的自协方差和自相关系数定义如下：

          ![](https://ws2.sinaimg.cn/large/006tNc79gy1ftwkflkz52g306q00j0pe.gif)

          ![](https://ws4.sinaimg.cn/large/006tNc79gy1ftwkfj1c2zg304o0160p7.gif)

        - 有了上面的概念作为支撑，我们可以定义，如果如果时间序列在某常数附近波动且有常数均值和方差，此外，延迟k期的自协方差和自相关系数相等(另一个角度来看也就是延迟k期的序列变量间的影响程度是一样的)，则这样的序列是平稳序列。

        (2) 平稳性检验

        一般有两种检验方法，一种是根据时序图和自相关图的特征判断，这种方法使用广泛但是带有主观性，另一种是构造检验统计量，最常用的方法是单位根检验。

        - **关于单位根检验，书里一笔带过，这里写一下详细的意义：**

          **单位根**从何而来，**这要从差分方程讲起**。

          在一个只有单变量的模型/系统里，即 ![ARMA(p,q)](https://www.zhihu.com/equation?tex=ARMA%28p%2Cq%29) 模型，它本身是一个差分方程：

          ![X_{t}=a _{0}+\sum _{i=0}^{p}a _{i}X_{t-i}+\sum _{i=0}^{q}\theta _{i}\varepsilon _{t-i}](https://www.zhihu.com/equation?tex=X_%7Bt%7D%3Da+_%7B0%7D%2B%5Csum+_%7Bi%3D0%7D%5E%7Bp%7Da+_%7Bi%7DX_%7Bt-i%7D%2B%5Csum+_%7Bi%3D0%7D%5E%7Bq%7D%5Ctheta+_%7Bi%7D%5Cvarepsilon+_%7Bt-i%7D)

          而**平稳性**意味着满足了**差分方程的稳定性条件**，从而差分方程的齐次解是零。

          学过微分方程或者差分方程应该知道，有关![X_{t}](https://www.zhihu.com/equation?tex=X_%7Bt%7D) 的方程的解由两部分组成，分别是**齐次解和特解**。

          解的过程我们会用到**特征方程和特征根**。

          ![X_{t}=a _{0}+\sum _{i=0}^{p}a _{i}X_{t-i}+\sum _{i=0}^{q}\theta _{i}\varepsilon _{t-i}](https://www.zhihu.com/equation?tex=X_%7Bt%7D%3Da+_%7B0%7D%2B%5Csum+_%7Bi%3D0%7D%5E%7Bp%7Da+_%7Bi%7DX_%7Bt-i%7D%2B%5Csum+_%7Bi%3D0%7D%5E%7Bq%7D%5Ctheta+_%7Bi%7D%5Cvarepsilon+_%7Bt-i%7D)

          上述方程有 ![m](https://www.zhihu.com/equation?tex=m) 个重复根的齐次解为

          ![\alpha\sum_{i=1}^{m}{A_{i}t^{i}}+\sum_{i=1+m}^{p}{A_{i}}\alpha^{t}_{i}](https://www.zhihu.com/equation?tex=%5Calpha%5Csum_%7Bi%3D1%7D%5E%7Bm%7D%7BA_%7Bi%7Dt%5E%7Bi%7D%7D%2B%5Csum_%7Bi%3D1%2Bm%7D%5E%7Bp%7D%7BA_%7Bi%7D%7D%5Calpha%5E%7Bt%7D_%7Bi%7D)

          其中,  ![A_{i}](https://www.zhihu.com/equation?tex=A_%7Bi%7D) 是任意常量， ![\alpha_{i}](https://www.zhihu.com/equation?tex=%5Calpha_%7Bi%7D) 是不同的特征根， ![\alpha](https://www.zhihu.com/equation?tex=%5Calpha) 是重复根。这里是 ![\alpha](https://www.zhihu.com/equation?tex=%5Calpha) 不是 ![a](https://www.zhihu.com/equation?tex=a) (第二个是英文字母a)。

          如果这个齐次根的任何一部分不是零，则这个差分方程的解的均值、方差和协方差就会依赖于时间 ![t](https://www.zhihu.com/equation?tex=t) 

          ![X_{t}](https://www.zhihu.com/equation?tex=X_%7Bt%7D) 的特解为

          ![X_{t}=(a_{0}+\sum_{i=0}^{q}\beta_{i}\varepsilon_{t-i})/(1-\sum_{i=1}^{p}a_{i}L^{i})](https://www.zhihu.com/equation?tex=X_%7Bt%7D%3D%28a_%7B0%7D%2B%5Csum_%7Bi%3D0%7D%5E%7Bq%7D%5Cbeta_%7Bi%7D%5Cvarepsilon_%7Bt-i%7D%29%2F%281-%5Csum_%7Bi%3D1%7D%5E%7Bp%7Da_%7Bi%7DL%5E%7Bi%7D%29)

          把它展开会得到一个 ![MA(\infty)](https://www.zhihu.com/equation?tex=MA%28%5Cinfty%29) 过程，我们需要让这个展开收敛，这样差分方程才能满足稳定性条件。

          所以需要有 ![1-\sum_{i=0}^{p}{a_{i}L^{i}}=0](https://www.zhihu.com/equation?tex=1-%5Csum_%7Bi%3D0%7D%5E%7Bp%7D%7Ba_%7Bi%7DL%5E%7Bi%7D%7D%3D0) 的根在单位圆外，其等价于

          ![\alpha^{p}-\sum_{i=1}^{p}{a_{i}\alpha^{p-i}}=0](https://www.zhihu.com/equation?tex=%5Calpha%5E%7Bp%7D-%5Csum_%7Bi%3D1%7D%5E%7Bp%7D%7Ba_%7Bi%7D%5Calpha%5E%7Bp-i%7D%7D%3D0) 的根在单位圆内。

          可以推得**平稳性的必要条件是** ![\sum _{i=1}^{p}a _{i}<1](https://www.zhihu.com/equation?tex=%5Csum+_%7Bi%3D1%7D%5E%7Bp%7Da+_%7Bi%7D%3C1) **，充分条件是** ![\sum _{i=1}^{p}\left| a _{i} \right|<1](https://www.zhihu.com/equation?tex=%5Csum+_%7Bi%3D1%7D%5E%7Bp%7D%5Cleft%7C+a+_%7Bi%7D+%5Cright%7C%3C1)。

          **单位根检验**就是检验该差分方程的特征方程的各个特征根是否小于1，即是否在单位圆内。

        - 时序图检验：根据平稳序列方差和期望都为一个常数的性质，我们观察时序图是否在一个常数范围波动，并且观察波动范围是否有界。如果有明显的趋势性和周期性那就不是平稳序列。

        - 自相关图检验：平稳序列具有短期相关性，这个短期体现在只有近期值对现在值影响较大，像个越远的远期值对现时值的影响越小。随着延迟期数k的增加，平稳序列的自相关系数 ![\rho_k](https://www.zhihu.com/equation?tex=%5Crho_k)  

          (也就是延迟k期)会较快的趋向于0，并在0处随机波动。而非平稳序列的自相关系数衰减较慢。

   2. 白噪声(纯随机性)检验

      如果一个序列是纯随机序列，那么它的序列值之间没有关联性，所以自协方差等于0，但这是理论上的情况，实际情况下它的值是无限接近于0，并在0附近随机扰动。

      白噪声检验一般构造统计量来进行假设检验，常用统计量有Q统计量和LB统计量，由样本的各延期自相关系数可以计算的统计量和相应的p值，如果p值显著大于显著性水平a，则表示该序列不能拒绝它是纯随机序列的原假设，即说明它是纯随机序列，可以停止对该序列的分析。

3. 平稳时间序列分析

   - ARMA模型，全称自回归移动平均模型，是最常用的拟合平稳序列的模型。它可以细分为AR, MA, ARMA三大类，但都可以看做是多元线性回归模型。

   - 先放上三个模型的识别原则

     ![](https://ws2.sinaimg.cn/large/006tNc79gy1ftwocifp8uj30kn03tdgv.jpg)

   - 关于截尾性和拖尾性，这两个性质是判断使用何种模型的重要依据，在后面会以图形实例来解释，单纯讲概念有点让人头大，这里你可以暂时带着疑问往下看。

   1. AR模型

      具有下列结构的p阶自回归模型，记为AR(p):

      ![](https://ws4.sinaimg.cn/large/006tNc79gy1ftwn1tdyw8g30a400i0sh.gif)

      其含义就是t时刻的随机变量Xt是前p期随机变量的多元线性回归，后面加一个当前期的随机干扰。

      - AR(p)模型的性质

      ![](https://ws2.sinaimg.cn/large/006tNc79gy1ftwnrg5atej30kw034gmm.jpg)

   2. MA模型

      具有下列结构的q阶自回归模型，记为MA(q):

      ![](https://ws4.sinaimg.cn/large/006tNc79gy1ftwnxweczmg309700i0p5.gif)

      t时刻的随机变量Xt是前q期的随机扰动的多元线性函数，误差项是当前期的随机扰动。我们认为此模型下Xt是受过去q期的误差项的影响。

      - MA(q)模型的性质

        ![](https://ws2.sinaimg.cn/large/006tNc79gy1ftwnrgbiiyj30kp02qjs9.jpg)

   3. ARMA模型

      具有下列结构的自回归移动平均模型，记为ARMA(p, q):

      ![](https://ws2.sinaimg.cn/large/006tNc79gy1ftwo3wjvahg30fq00igld.gif)

      t时刻的随机变量Xt是前p期随机变量和前q期的随机扰动的多元线性函数，误差项是当前期的随机扰动。Xt受过去p期序列值和q期扰动的共同影响。

      - q = 0时是AR(p)模型，p = 0 时是MA(q)模型

      - ARMA(p, q)性质

        ![](https://ws4.sinaimg.cn/large/006tNc79gy1ftwnrfpzqdj30kp02saax.jpg)

   

4.  平稳时间序列建模

   我们可以根据上文的知识，总结出一套平稳序列的建模方法，流程图如下：

   ![](https://ws2.sinaimg.cn/large/006tNc79gy1ftwoenhvlij307z0ag3zp.jpg)

   可以总结成如下步骤：

   1）计算ACF(自相关系数)和PACF(偏自相关系数)

   2）ARMA模型识别也就是定阶

   3）在选择出来的模型中估计位置参数并检验

   4）对模型进行优化

   5）应用

5. 非平稳时间序列分析

   - 实际生活中，平稳序列是少之又少的，大多数情况下我们遇到的都是非平稳序列。

   - 对非平稳序列的分析方法可以分为两大类，一是确定性因素分解的时序分析，二是随机时序分析。

     确定性因素分解的方法是根据长期趋势，季节变动，循环变动，随机波动四个因素的综合影响，其中长期趋势和季节变动的规律较容易提取，而由随机因素导致的波动很难确定，这种对随机信息的浪费会导致模型的欠拟合。而在此基础上的随机时序分析法的发展就是为了弥补上面方法的不足。

   - 随机时序分析可以建立的模型有ARIMA模型，残差自回归模型，季节模型和异方差模型等，这一篇我们重点总结ARIMA模型。

     

   

   1. 差分运算

      1）p阶差分

      相距一期的两个序列值之间的减法运算称为1阶差分运算。

      2）k步差分

      相距k期的两个序列值之间的减法运算称为k步差分运算。

   2. ARIMA模型

      差分运算具有强大的确定性信息提取能力，许多非平稳序列经过差分之后会显示出平稳序列的性质，这样的序列被称为差分平稳序列，对差分平稳序列可以用ARMA模型拟合，步骤流程图如下：

      ![](https://ws3.sinaimg.cn/large/0069RVTdgy1ftxtx3z5w2j309m07hq3p.jpg)

## 实例分析

介绍完整个时间序列分析如何建模之后，我们运用所学用一个例子来更形象的进行分析。我们从参考书中附录部分拿到了2015/1/1-2015/2/6某餐厅的销售数据进行建模，数据样本大概如下：

![](https://ws4.sinaimg.cn/large/0069RVTdgy1ftxu0ujsxyj304x0d1gm1.jpg)

1. 平稳性分析

   拿到一个数据，我们不确定它是平稳序列还是非平稳序列，所以先对它做平稳性检验，回顾上面的内容，平稳性检验的方法有时序图检验，自相关图检验，和单位根检验，下面来应用一下。

   1. 时序图和自相关图检验

      ```python
      #!/usr/bin/env python
      # -*- coding: utf-8 -*-
      __author__ = "MambaHJ"
      
      import pandas as pd
      import os
      
      current_dir = os.getcwd()
      root_dir = os.path.dirname(current_dir)
      data_path = os.path.join(root_dir, "data/arima_data.xls")
      data = pd.read_excel(data_path, index_col=u'日期')
      
      import matplotlib.pyplot as plt
      # plt.rcParams['font.sans-serif'] = ['SimHei']
      # plt.rcParams['axes.unicode_minus'] = False
      # 绘制时序图
      data.plot()
      plt.legend("sales") 	# 标签
      plt.xlabel("date")
      plt.ylabel("sales")
      
      # 绘制自相关图
      from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
      plot_acf(data)
      plt.show()
      ```

      时序图：

      ![](https://ws2.sinaimg.cn/large/0069RVTdgy1ftxwuz8f4jj30hs0dc0t4.jpg)

      自相关图：

      ![](https://ws3.sinaimg.cn/large/0069RVTdgy1ftxwvgk5c9j30hs0dcq38.jpg)

      由图片可以看出，时序图具有明显的趋势性，自相关图并没有很快趋于0，且衰减速度较慢，可以主观分辨出这是一个非平稳序列，但是为了以防万一，我们继续做一个单位根检验：

      ```python
      # 单位根检验
      from statsmodels.tsa.stattools import adfuller as ADF
      print(u"原始序列的单位根检验结果：{}".format(ADF(data[u'销量'])))
      # 返回值依次是adf, pvalues, usedlag, nobs, critical values, icbest, regresults, resstore
      ```

      返回结果：

      ```
      原始序列的单位根检验结果：(1.8137710150945263, 0.99837594215142644, 10, 26, {'1%': -3.7112123008648155, '5%': -2.9812468047337282, '10%': -2.6300945562130176}, 299.46989866024177)
      ```

      注意我们的原假设是存在单位根，**单位根统计量对应的p的值为0.998显著大于0.05**所以不能拒绝原假设，即存在单位根，所以这个序列是非平稳序列(同时要搞清楚，非平稳序列不等于白噪声序列)

      2. 对于非平稳序列，我们首先要对其进行差分运算，把它转化成平稳序列：

      ```python
      # 对非平稳序列建模首先要进行差分运算，把它差分成平稳序列
      # 差分后的结果
      D_data = data.diff().dropna()
      D_data.columns = [u'销量差分']
      D_data.plot()	# 时序图
      plt.ylabel("diff_sales")
      plt.legend("diff_sales")
      plot_acf(D_data)	# 自相关图
      plt.show()
      print(u"差分序列的单位根检验结果：{}".format(ADF(D_data[u'销量差分'])))
      ```

      差分后的时序图：

      ![](https://ws4.sinaimg.cn/large/006tKfTcgy1ftysr2yoj4j30hs0dcmxo.jpg)

      自相关图：

      ![](https://ws4.sinaimg.cn/large/006tKfTcgy1ftysr48k5gj30hs0dcdg1.jpg)

      偏自相关图：

      ![](https://ws3.sinaimg.cn/large/006tKfTcgy1ftytlv7154j30hs0dcglr.jpg)

      和差分前的图形相比，时序图可以明显的观察到在一个常数范围波动，且自相关图很快趋于0，并在0附近波动。再来看一看单位根检验的结果：

      ```
      差分序列的单位根检验结果：(-3.1560562366723541, 0.022673435440048757, 0, 35, {'1%': -3.6327426647230316, '5%': -2.9485102040816327, '10%': -2.6130173469387756}, 287.59090907803341)
      ```

      **可以看到p值为0.0226<0.05, 可以拒绝原假设**，说明经过一阶差分之后的序列是平稳序列。接下来，我们要进行白噪声检验，这一步关系到我们有没有必要继续分析下去。

      3. 白噪声检验

         ```python
         # 白噪声检验
         from statsmodels.stats.diagnostic import acorr_ljungbox
         # 返回统计量和p值
         print(u"差分序列的白噪声检验结果为：{}".format(acorr_ljungbox(D_data, lags=1)))
         ```

         结果:

         ```
         差分序列的白噪声检验结果为：(array([ 11.30402222]), array([ 0.00077339]))
         ```

         p值为0.000773<0.05, 可以拒绝原序列是一个白噪声序列的假设，因此我们下面的分析就是有意义的了。

      4. 模型定阶

         这一步是整个建模中的核心部分，原序列经过差分之后变成了一个平稳非白噪声序列，我们要做的就是用ARMA模型去拟合它。

         1. 人为识别

            对于本题中的数据，我们可以观察到它的自相关图在q=1，之后落入安全区域内，显示除了1阶截尾性，而偏自相关图显示出拖尾性，可以考虑用MA(1)模型去拟合。

         2. 相对最优模型识别

            人为识别可能有误差，所以还有一种方法是计算ARMA(p,q)，计算p和q均小于等于3的所有组合的bic信息量，取使bic信息量达到最小的模型阶数。

            有几个注意点：

            - 对差分序列做MA（1）模型拟合，而想用的就要对原序列做ARIMA（0,1,1）模型拟合
            - ARIMA（p,d,q）三个系数分别为：p是自回归(AR)的项数，d是差分(I)的系数，q是移动平均(MA)的项数

            ```python
            from statsmodels.tsa.arima_model import ARIMA
            # 模型定阶
            data[u'销量'] = data[u'销量'].astype(float) 	# 注意训练时序模型时要传进去的是float型
            pmax = int(len(D_data)/10)		# 一般阶数不超过长度的十分之一
            qmax = int(len(D_data)/10)
            bic_mat = []
            for p in range(pmax+1):
            	tmp = []
            	for q in range(qmax+1):
            		try: #	拟合原序列
            			# 人为观察出来用MA(1)模型拟合差分序列，即对1阶差分后的原数据进行ARIMA(p,1,q)模型
            			tmp.append(ARIMA(data, (p,1,q)).fit().bic)
            		except:
            			tmp.append(None)
            	bic_mat.append(tmp)
            
            bic_mat = pd.DataFrame(bic_mat)
            print(bic_mat)
            p,q = bic_mat.stack().idxmin()
            print(u"bic最小的p值和q值为：{}，{}".format(p,q))
            # 建立ARIMA（0，1，1）模型
            model = ARIMA(data, (p,1,q)).fit()
            print(model.summary2())
            # 作为期5天的预测，返回预测结果，标准误差，置信区间
            print(model.forecast(5))
            ```

            **运行结果：**

            1. bic信息矩阵：

               ```
                           0           1           2           3
               0  432.068472  422.510082  426.088911  426.595507
               1  423.628276  426.073601         NaN         NaN
               2  426.774824  427.395893         NaN         NaN
               3  430.317524         NaN         NaN  436.478109
               ```

            2. p = 0 , q = 1

            3. 总结报告：

               ```
                                          Results: ARIMA
               ====================================================================
               Model:              ARIMA            BIC:                 422.5101  
               Dependent Variable: D.销量             Log-Likelihood:      -205.88   
               Date:               2018-08-05 15:31 Scale:               1.0000    
               No. Observations:   36               Method:              css-mle   
               Df Model:           2                Sample:              01-02-2015
               Df Residuals:       34                                    02-06-2015
               Converged:          1.0000           S.D. of innovations: 73.086    
               AIC:                417.7595         HQIC:                419.418   
               ----------------------------------------------------------------------
                              Coef.    Std.Err.     t      P>|t|     [0.025    0.975]
               ----------------------------------------------------------------------
               const         49.9562    20.1390   2.4806   0.0182   10.4845   89.4279
               ma.L1.D.销量     0.6710     0.1648   4.0712   0.0003    0.3480    0.9941
               -----------------------------------------------------------------------------
                                Real           Imaginary          Modulus          Frequency
               -----------------------------------------------------------------------------
               MA.1           -1.4902             0.0000           1.4902             0.5000
               ====================================================================
               ```

            4. 预测：

               ```
               (array([ 4873.96662161,  4923.92285197,  4973.87908233,  5023.83531269,
                       5073.79154305]), array([  73.08574317,  142.32679364,  187.5428125 ,  223.80280796,
                       254.95703007]), array([[ 4730.72119722,  5017.21204601],
                      [ 4644.96746241,  5202.87824154],
                      [ 4606.30192428,  5341.45624039],
                      [ 4585.18986944,  5462.48075594],
                      [ 4574.0849465 ,  5573.4981396 ]]))
               ```

               - 第一个array是预测结果
               - 第二个是误差
               - 带三个是置信区间

## 补充一些python中主要的时序算法

实现时序分析，主要用到statsmodels库，下面是它的常用接口:

```
acf() 计算自相关系数 statsmodels.tsa.stattols

plt_acf() 画自相关系数 statsmodels.graphics.tsaplots

pacf() 计算片相关系数 statsmodels.tsa.stattols

plot_acf() 画偏相关系数 statsmodels.graphics.tsaplots

adfuller() 对观测值序列进行单位根检验 statsmodels.tsa.stattols//ADF test

diff() 对观测值进行查分计算 pandas对象自带的方法

ARIMA() 创建一个ARIMA序列模型 statsmodels.tsa.arima_model

summary()&summaty2 给出一分ARIMA模型的报告 ARIMA模型对象自带方法

aic/bic/hqic 计算ARIMA模型的AIC/BIC/HQIC指标值 ARIMA模型对象自带方法

froecast() 应用构建的时间序列进行预测 ARIMA模型对象自带方法

acorr_ljungbox() Ljung-Box检验，检验是否为白噪声 statsmodels.stats.diagnostic
```





