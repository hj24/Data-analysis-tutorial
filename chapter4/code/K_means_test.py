import  pandas as pd
from sklearn.cluster import KMeans

inputfile = 'data/data/business_circle.xls'
outputfile = 'data/data/KMeans_output.xls'

k=3
iter=500
data = pd.read_excel(inputfile, index_col='基站编号')
data_std = 1.0*(data - data.mean())/(data.max()-data.min())
print(data_std.head(5))
model = KMeans(n_clusters=k, n_jobs=4, max_iter=iter)
# 开始聚类
model.fit(data_std)
# 各类别个数
r1 = pd.Series(model.labels_).value_counts()
r2 = pd.DataFrame(model.cluster_centers_)
print(r1)
print(r2)
r = pd.concat([r2,r1], axis=1)
# 重命名表头
r.columns = list(data.columns) + [u'类别数目']
print(r)
# 详细输出原始数据及其类别
res = pd.concat([data, pd.Series(model.labels_, index=data.index)],axis=1)
res.columns = list(data.columns) + [u"聚类类别"]
res.to_excel(outputfile)

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
t = TSNE()
t.fit_transform(data_std)
t = pd.DataFrame(t.embedding_, index=data_std.index)
print(t.head(5))
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
d = t[res[u'聚类类别'] == 0]
plt.plot(d[0],d[1],'r.')
d = t[res[u'聚类类别'] == 1]
plt.plot(d[0],d[1],'go')
d = t[res[u'聚类类别'] == 2]
plt.plot(d[0],d[1],'b*')
plt.show()
plt.savefig('Consequence/label.png')



