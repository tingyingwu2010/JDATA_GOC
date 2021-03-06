# -*- coding:utf-8 -*-
# @Time     :2018/6/17 17:41
# @Author   :gwl
# @File     :dbscan.py

# DBSCAN聚类算法 密度聚类模型

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# 获取make_blobs 数据
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4, random_state=0)
# 数据预处理
X = StandardScaler().fit_transform(X)

# 执行DBSCAN算法
db = DBSCAN(eps=0.3, min_samples=10).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
# 标记核心对象，后面作图用
core_samples_mask[db.core_sample_indices_] = True
# 算法得出聚类标签， -1代表样本噪声点，气其余值表示样本点所属的类
labels = db.labels_
# 获取聚类的数量
n_cluster_ = len(set(labels)) - (1 if -1 in labels else 0)
# 输出算法性能的信息
print('Estimated Number of cluster: %d' % n_cluster_)
print('Homogeneity: %0.3f' % metrics.homogeneity_score(labels_true, labels))
print('Completeness: 0.3%f' % metrics.completeness_score(labels_true, labels))
print('Adjusted Rand Index: 0.3%f' % metrics.adjusted_rand_score(labels_true, labels))
print('Adjusted Mutual Information: 0.3%f' % metrics.adjusted_mutual_info_score(labels_true, labels))
print('Silhouette Coefficient: 0.3%f' % metrics.silhouette_score(X, labels))

# 作图
# 黑色标记噪声点
unique_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
i = -1
# 标记样式 ，x表示噪声点
marker = ['v', '^', 'o', 'x']
for k, col in zip(unique_labels, colors):
    if k == -1:
        # 黑色标记噪声点
        col = 'k'
    class_member_mask = (labels == k)
    i += 1
    if i >= len(unique_labels):
        i = 0
    # 绘制核心对象
    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], marker[i], makerfacecolor=col, makeredgecolor='k', marksize=14)
    # 绘制非核心对象
    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[: 1], marker[i], makerfacecolor=col, makeredgecolor='k', marksize=6)
plt.title('Estimated number of clusters: %d' % n_cluster_)
plt.show()
