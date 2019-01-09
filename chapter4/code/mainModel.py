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