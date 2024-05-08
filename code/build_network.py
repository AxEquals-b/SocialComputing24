import data_proccess as data
import numpy as np
import matplotlib.pyplot as plt

# 使用timeline上的一部分投票数据生成网络
# date: 时间前缀，筛选用于生成网络的vote数据。如'2000'或'2000-06-17'
# degree: 每个节点的度数。使用默认值0时，不进行度数控制，生成的将会是一个稠密图
class VoteNetwork:
    def __init__(self, timeline, date, degree = 0):
        n = len(timeline.members)

        # 用于描述两人投票的相关性，若其中任意一人弃权则记为0 
        # 否则，两人意见相同记为1, 意见不同记为-1 
        # 对角线元素edges[i, i]即为此人总共的投票次数
        self.edges = np.zeros((n, n))
        for votes in timeline.at(date):
            # 记录投票相关性
            yn = len(votes.Y)
            nn = len(votes.N)
            # 相同投票，相关性 +1 
            for i in range(yn):
                for j in range(yn):
                    self.edges[timeline.mem2idx[votes.Y[i].member], timeline.mem2idx[votes.Y[j].member]] += 1
            for i in range(nn):
                for j in range(nn):
                    self.edges[timeline.mem2idx[votes.N[i].member], timeline.mem2idx[votes.N[j].member]] += 1
            # 相反投票，相关性 -1
            for i in range(yn):
                for j in range(nn):
                    self.edges[timeline.mem2idx[votes.Y[i].member], timeline.mem2idx[votes.N[j].member]] -= 1
                    self.edges[timeline.mem2idx[votes.N[j].member], timeline.mem2idx[votes.Y[i].member]] -= 1
        if degree == 0:
            degree = n
        # 仅保留权重最大的边
        sorted_indices = np.argsort(-np.abs(self.edges), axis=1)
        for i in range(len(self.edges)):
            row_indices_to_keep = sorted_indices[i][degree:]  
            self.edges[i, row_indices_to_keep[:]] = 0  
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                # 归一化并防止除0异常
                self.edges[i, j] /= max(self.edges[i, i], 1)
