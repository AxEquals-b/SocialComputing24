import data_proccess as data
import build_network as net
import matplotlib.pyplot as plt
import numpy as np

data.init("../data")
# 从votes.json读入的原始数据，这里可以做训练集/测试集划分
votes = data.votes
# 将votes按时间轴组织为更合适的数据结构
timeline = data.VoteTimeline(votes)
# 对每个存在投票的月份构建网络
# 也可以使用 'YYYY' 或 'YYYY-MM-DD' 来按年份或日期粒度来构建网络
prev_net = None
for date in timeline.time_prefixes("YYYY"):
    print(f"time: {date}")
    # degree用于在网络构建过程中限制节点的出度最大值
    # 不添加degree参数时，不限制节点出度，此时产生的是稠密图
    vote_net = net.VoteNetwork(timeline, date, degree = 30, prev = prev_net, fade_rate = 0.3, weak_link = 0.5)
    plt.imshow(vote_net.edges, cmap='coolwarm', vmin=-1, vmax=1)
    plt.colorbar() 
    plt.show()
    prev_net = vote_net


