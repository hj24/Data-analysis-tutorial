# 基于基站定位数据的商圈分析

## 实践过程

​	首先，我们明确分析模型的目标为基于定位数据的商圈分析，这就使得我们需要的数据应集中服务于该目标。因此，我们要对数据进行预处理：

- 我们从移动运营商得到基站定位的相关数据，并对其进行初步分析，剔除与目标无关的数据，进行数据清洗降低维度。

- 清洗后的数据仍可能存在相互关联的情况，因此我们需要合并相互关联的属性以及作用重叠的属性。

- 清洗合并后的数据直观上与目标的关联性仍是比较小的，所以我们需要分析归纳处最相关的属性，并用已有的数据去量化它得到新的属性，并将其标准化，以防不同数量级造成的影响。

  ​	处理完数据之后开始进行正式的分析，为了有定位数据分析商圈，我们需要根据已有的数据进行无监督的聚类，根据居民的移动趋势划分商圈类别。例如，上班族白天在某地停留时间长，而居民在住宅区凌晨停留时间长，通过类似这样的指标很容易可以进行划分。

  ​	此外我们还需将各级商圈数据进行可视化以便更直观的分析数据结论。

  ​	综上，在此篇分析中，我们综合运用了离差标准化，日均停留时间量化模型对数据进行了预处理，并使用层次聚类法训练模型，对商圈进行了分类来综合评价分析数据。

## 数据预处理

1. 数据抽取

   ​	从移动通信运营商的接口上解析处理并过滤用户属性之后得到位置数据，数据从2014-1-1开始至2014-6-30结束，数据截图如下：

   ![原始数据](https://ws2.sinaimg.cn/large/006tKfTcgy1fs3z7z8fuqj30kt0bsjwu.jpg)

2. 数据规约

   ​	原始数据维度较多，但仔细审视数据之后会发现网络类型、LOC编号和信号类型对于我们的定位数据并没有影响，因此考虑将其删除。此外在时间尺度上，衡量用户的停留时间并不需要精确到毫秒，所以我们可以将毫秒这一属性删除并且，为了减少维度，我们把年月日合并到一个维度上即日期，处理之后的数据可参考下表：

   ![规约后的数据](https://ws2.sinaimg.cn/large/006tKfTcgy1fs3xkvi463j30l20eh794.jpg)

3. 数据变换

   ​	我们挖掘的目标是高价值的商圈，分析高价值商圈的特点，我们可以的出如下结论：高价值商圈具有人流量大和人均停留时间长的特点。

   ​	进一步考虑，在白天，写字楼由于要供上班族使用，所以它的基站范围基本固定，停留时间也相对较长，相应的，晚上下班后住宅区居民所处的基站范围也相对固定且停留时间较长，所以我们需要划分以下指标并进行量化：

   - 工作日人均停留时间及量化

     ​	工作日居民平均上班时间：9：00-18：00，所以工作日人均停留时间是计算在此时间内用户在该基站范围内的平均时间。

     量化公式：

     ![f1](https://ws3.sinaimg.cn/large/006tKfTcgy1fs406ytmifj308k01kmwx.jpg)

   - 凌晨人均停留时间：

     ​	凌晨人均停留时间00：00-07：00，该指标表示住宅区基站的人流特征。

     量化公式：

     ![f2](https://ws4.sinaimg.cn/large/006tKfTcgy1fs40cyje19j307601kgld.jpg)

   - 周末人均停留时间：

     ​	高价值商圈人均停留时间在周末会大幅增加。

     量化公式：

     ![f3](https://ws2.sinaimg.cn/large/006tKfTcgy1fs40gt6aqgj308l01kgld.jpg)

   - 日均人流量：

     量化公式：

     ![f4](https://ws2.sinaimg.cn/large/006tKfTcgy1fs40gxg6mgj306401k741.jpg)

     L为观测时间，基站和用户个数分别为N和M，用户i在j天经过的基站有n1，n2，n3。工作日、凌晨、周末分别对应，weekday，night，weekend在基站是否停留为stay。

   - 得到变化后的数据，保存到/data/business_circle.xls中

     ![fig1](https://ws1.sinaimg.cn/large/006tKfTcgy1fs40qc6q7wj309r0j2dhc.jpg)

4. 数据标准化

   ​	由于各属性之间差异较大，在进行聚类前需要进行离差标准化来消除数量级带来的影响。

   离差标准化公式：

   ![f5](https://ws2.sinaimg.cn/large/006tNc79gy1fs4102nrv6j303z0130l1.jpg)

   代码：

   ```python
   import pandas as pd
   #参数初始化
   filename = '../data/business_circle.xls' #原始数据文件
   standardizedfile = '../tmp/standardized.xls' 
   
   data = pd.read_excel(filename, index_col = u'基站编号') #读取
   
   data = (data - data.min())/(data.max() - data.min()) #标准化
   data = data.reset_index()
   
   data.to_excel(standardizedfile, index = False) #保存结果
   ```

   标准化之后的数据：

   ![fig2](https://ws3.sinaimg.cn/large/006tNc79gy1fs413phqdvj309r0cbabl.jpg)

5. 心得

   在对该数据集进行分析和清洗的过程中，本人收获了如下经验：

   1. 对于维度较多的数据，首先思考剔除和所求目标无关的数据，并将相关的数据进行合并以达到降维的目的，对于数据集复杂且维度巨大的数据，可以考虑用主成分分析算法来解决。
   2. 对于数据尺度不同，且相差较大的数据要进行标准化，以防数量级对后续分析造成的影响。

## 数据分析与挖掘解读

1. 聚类

   ​	为了研究基于定位数据对商圈进行分类，我们自然的想到对经过预处理的数据，采用层次聚类算法，首先画出它的谱系聚类图谱：

   ![聚类图](https://ws1.sinaimg.cn/large/006tNc79gy1fs44m99053j30hs0dc0t5.jpg)

   代码：

   ```python
   import pandas as pd
   
   stardFile = 'data/data/standardized.xls'
   data = pd.read_excel(stardFile,index_col=u'基站编号')
   print(data.head(3))
   
   import matplotlib.pyplot as plt
   # scipy中的层次聚集函数
   from scipy.cluster.hierarchy import linkage,dendrogram
   
   Z = linkage(data, method='ward', metric='euclidean') #谱系聚类图
   P = dendrogram(Z, 0)
   plt.show()
   plt.savefig('Consequence/fig_4')  # 保存聚类树图
   ```

   ​	从图中可以初步看出，我们的聚类类别为3，下面进一步用聚类算法求出详细数据并对商圈进行划分：

   代码：

   ```python
   # 层次聚类算法
   import pandas as pd
   
   # 参数初始化
   standardizedfile = 'data/data/standardized.xls' 
   k = 3  # 聚类数
   data = pd.read_excel(standardizedfile, index_col=u'基站编号')  # 读取数据
   
   from sklearn.cluster import AgglomerativeClustering  # 导入sklearn的层次聚类函数
   
   model = AgglomerativeClustering(n_clusters=k, linkage='ward')
   model.fit(data)  # 训练模型
   
   # 详细输出原始数据及其类别
   r = pd.concat([data, pd.Series(model.labels_, index=data.index)], axis=1)  # 详细输出每个样本对应的类别
   r.columns = list(data.columns) + [u'聚类类别']  # 重命名表头
   
   import matplotlib.pyplot as plt
   
   plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
   plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
   
   style = ['ro-', 'go-', 'bo-']
   xlabels = [u'工作日人均停留时间', u'凌晨人均停留时间', u'周末人均停留时间', u'日均人流量']
   pic_output = 'Consequence/fig_'  # 聚类图文件名前缀
   
   for i in range(k):  # 逐一作图，作出不同样式
       plt.figure()
       tmp = r[r[u'聚类类别'] == i].iloc[:, :4]  # 提取每一类
       for j in range(len(tmp)):
           plt.plot(range(1, 5), tmp.iloc[j], style[i])
   
       plt.xticks(range(1, 5), xlabels, rotation=20)  # 坐标标签
       plt.title(u'商圈类别%s' % (i + 1))  # 我们计数习惯从1开始
       plt.subplots_adjust(bottom=0.15)  # 调整底部
       plt.savefig(u'%s%s.png' % (pic_output, i + 1))  # 保存图片
   ```

2. 分析

   ​	针对聚类的结果，我们画出3个特征的折线图，分别对应三种类别的商圈（weekday对应工作日人均停留时间、night对应凌晨人均停留时间、weekend对应周末人均停留时间、average对应日均人流量）：

   - 商圈1

     ![1](https://ws2.sinaimg.cn/large/006tNc79gy1fs44x96m0lj30hs0dc0tl.jpg)

     ​	如图商圈1的人流量大，日均流量大也就是说每天都有稳定的人数停留，适合运营商的促销活动。

   - 商圈2

     ![2](https://ws4.sinaimg.cn/large/006tNc79gy1fs44xc1nffj30hs0dcwfo.jpg)

     ​	从上图分析出，凌晨人均停留时间和周末比较大，而工作日比较小，对应住宅区，环境比较安静，停车方便，地价也不高。该类商业圈附适合经营居民日常生活需要的便利品，以超市及便利店为主。

   - 商圈3

     ![3](https://ws3.sinaimg.cn/large/006tNc79gy1fs44xkmte6j30hs0dc3z4.jpg)

     ​	从商圈3的分布折线可以看出，这类商圈工作日人均停留时间非常大，但凌晨和周末则很短，该类商圈属于辅助商业区，对应上班族的工作区域。平时人流量少，店铺类型及所销售的商品大体上同商业中心区相同，只是店铺数量较少，经营商品的种类也较少。

3. 总结

   ​	整个实践过程中，我们通过基站的定位数据，清洗、合并、重新量化，将它提取成了符合我们需求的和商圈紧紧关联的数据，在此基础上我们进行了聚类。由聚类的结果，我们分析出了上面的观点，总结下来如下：

   1. 该地区商圈主要分为三大类，一类是以住宅区为中心的商业圈，适合便利型的超市，居民生活用品的经营和销售，此外还可以发展家具、宠物等产业贴近居民生活。

   2. 第二类则是主要服务于上班族的办公型商业中心，该类商圈适合各种企业的入驻，是一个城市的竞争力的核心，此外，该地区适合零售业，店铺类型不一定要齐全但要符合上班族的需求，如美食城、数码3C用品店等。

   3. 最后一类是日均人流量大的商业区，对应一个城市的休闲娱乐中心，不管是工作日还是周末都有稳定的人流，在周末还有上升趋势。此地区适合各大销售品牌入驻，适合促销活动，需要建立完善的娱乐休闲产业链满足城市居民的休闲需求。

      ​	以上便是整个实践的分析，通过这个完整的实践，本人的数据分析能力也进一步得到提升，并熟悉了更多算法。