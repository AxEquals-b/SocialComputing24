# 将json数据读入并转为更合适的数据结构
import json

class Meeting:
    def __init__(self):
        self.cosponsors = []

    def add_data(self, jsonData):
        self.id = jsonData['meeting']
        if jsonData['subclub'] == 0:
            self.sub0 = jsonData['members']
        else:
            self.sub1 = jsonData['members']

    def add_cosponsor(self, cosponsor):
        self.cosponsors.append(cosponsor)

class Cosponsor:
    def __init__(self, jsonData):
        self.bill_id = jsonData['bill_id']
        self.bill_type = jsonData['bill_type']
        self.dates = jsonData['actions_dates']
        self.sponsor = jsonData['sponsor']
        self.cosponsors = jsonData['cosponsors']

# 一张选票
class Vote:
    def __init__(self, jsonData):
        self.date = jsonData['date']
        self.bill_id = jsonData['bill_name']
        self.bill_type = jsonData['bill_type']
        self.member = jsonData['id']
        self.group = jsonData['group']
        self.district = jsonData['district']
        self.vote = jsonData['vote']
# 一次表决的所有选票数据
class Votes:
    def __init__(self):
        self.Y = []
        self.N = []
        self.NV = []
    def add_vote(self, vote):
        if vote.vote == 'Y':
            self.Y.append(vote)
        elif vote.vote == 'N':
            self.N.append(vote)
        elif vote.vote == 'NV':
            self.NV.append(vote)
# 按时间线组织的所有选票数据
class VoteTimeline:
    def __init__(self, votes):
        # 曾经参加过投票的所有用户
        self.members = set()
        # 按顺序排列的所有日期
        self.dates = set()
        # (bill_id, date) -> Votes
        self.votes = {}
        for vote in votes:
            self.add_vote(vote)
        self.dates = sorted(list(self.dates))
        self.members = sorted(list(self.members))
        # members的逆映射，即member_id映射到members内的下标
        self.mem2idx = {}
        for i in range(len(self.members)):
            self.mem2idx[self.members[i]] = i
    def add_vote(self, vote):
        self.dates.add(vote.date)
        self.members.add(vote.member)
        vote_key = (vote.bill_id, vote.date)
        if vote_key not in self.votes:
            self.votes[vote_key] = Votes()
        self.votes[vote_key].add_vote(vote)
    # 使用时间前缀匹配Votes数据
    def at(self, time_prefix):
        return (value for key, value in self.votes.items() if key[1][:len(time_prefix)] == time_prefix)
    def time_prefixes(self, prefix_format):
        result = set()
        for date in self.dates:
            result.add(date[:len(prefix_format)])
        return sorted(list(result))

# meeting_id -> Meeting
meetings = {}
# bill_id -> Cosponsor
cosponsors = {}
# (bill_id, bill_date) -> Vote
votes = []

def init(data_path):
    with open(f"{data_path}/members.json", "r") as f:
        jsonDatas = json.loads(f.read())
        for jsonData in jsonDatas:
            id = jsonData['meeting']
            if id not in meetings:
                meetings[id] = Meeting()
            meetings[id].add_data(jsonData)
    with open(f"{data_path}/cosponsors.json", "r") as f:
        jsonDatas = json.loads(f.read())
        for jsonData in jsonDatas:
            cosponsor = Cosponsor(jsonData)
            id = cosponsor.bill_id
            cosponsors[id] = cosponsor 
            meeting_id = id[len(id) - 3:]
            if meeting_id in meetings:
                meetings[meeting_id].add_cosponsor(cosponsor)
    with open(f"{data_path}/votes.json", "r") as f:
        jsonDatas = json.loads(f.read())
        for jsonData in jsonDatas:
            votes.append(Vote(jsonData))

