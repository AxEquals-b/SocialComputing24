import data_proccess as data
import numpy as np
import matplotlib.pyplot as plt

# 使用timeline上的一部分投票数据生成网络
# date: 时间前缀，筛选用于生成网络的vote数据。如'2000'或'2000-06-17'
# degree: 每个节点的度数。使用默认值0时，不进行度数控制，生成的将会是一个稠密图
# prev: 上一个时刻的图。若不传入，则不使用上一个时刻的网络数据，图与图之间没有联系
# fade_rate: 上一个时刻的图的权重比例。cur = cur + prev * fade_rate 
# weak_link: 在下一次迭代时，与邻居的邻居节点建立连接，新连接的权重为 (w1 * w2 * weak_link)。其中w1*w2是本地节点到邻居的邻居节点的路径上两条边的权重
class VoteNetwork:
    def __init__(self, timeline, date, degree = 0, prev = None, fade_rate = 0.6, weak_link = 0.2):
        n = len(timeline.members)

        # 用于描述两人投票的相关性，若其中任意一人弃权则记为0 
        # 否则，两人意见相同记为1, 意见不同记为-1 
        self.edges = np.zeros((n, n))
        for votes in timeline.at(date):
            # 记录投票相关性
            yn = len(votes.Y)
            nn = len(votes.N)
            y2i = []
            n2i = []
            for i in range(yn):
                y2i.append(timeline.mem2idx[votes.Y[i].member])
            for i in range(nn):
                n2i.append(timeline.mem2idx[votes.N[i].member])
            # 相同投票，相关性 +1 
            for i in range(yn):
                for j in range(yn):
                    self.edges[y2i[i], y2i[j]] += 1
            for i in range(nn):
                for j in range(nn):
                    self.edges[n2i[i], n2i[j]] += 1
            # 相反投票，相关性 -1
            for i in range(yn):
                for j in range(nn):
                    self.edges[y2i[i], n2i[j]] -= 1
                    self.edges[n2i[j], y2i[i]] -= 1
        # 对角线元素edges[i, i]即为此人总共的投票次数
        self.vote_cnt = np.zeros(n)
        for i in range(n):
            self.vote_cnt[i] = max(1, self.edges[i, i])
            self.edges[i, i] = 0
        for i in range(n):
            for j in range(n):
                self.edges[i, j] /= self.vote_cnt[i]
        if prev != None:
            self.edges += prev.edges * fade_rate
            self.edges += weak_link * np.dot(prev.edges, prev.edges) / n
        for i in range(n):
            self.edges[i, i] = 0
        if degree == 0:
            degree = n
        # 仅保留权重最大的边
        sorted_indices = np.argsort(-np.abs(self.edges), axis=1)
        for i in range(len(self.edges)):
            row_indices_to_keep = sorted_indices[i][degree:]  
            self.edges[i, row_indices_to_keep[:]] = 0  
#        weights = []
#        for i in range(n):
#            for j in range(n):
#                if self.edges[i, j] != 0:
#                    weights.append(self.edges[i, j])
#        plt.hist(weights, bins=30, edgecolor='black')
#        plt.xlabel('Value')
#        plt.ylabel('Frequency')
#        plt.title('Histogram of Data')
#        plt.grid(True)
#        plt.show()

