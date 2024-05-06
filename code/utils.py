import json

# 读取源数据
def readData():
    with open("../data/cosponsors.json", "r") as f:
        cosponsors = json.loads(f.read())
    with open("../data/members.json", "r") as f:
        members = json.loads(f.read())
    with open("../data/votes.json", "r") as f:
        votes = json.loads(f.read())
    return cosponsors, members, votes

# 获取提出过的提案，返回以bill_name为key，以True为value的dict
def get_sponsored_bills(cosponsors):
    cosponsor_bills = {}
    for sponsor in cosponsors:
        name = sponsor["bill_id"]
        if name not in cosponsor_bills:
            cosponsor_bills[name] = True
    return cosponsor_bills

# 获取投票过的提案，返回以bill_name为key，以True为value的dict
def get_voted_bills(votes):
    voted_bills = {}
    for vote in votes:
        name = vote["bill_name"]
        if name not in voted_bills:
            voted_bills[name] = True
    return voted_bills

# 获取提出过并投票过的提案，返回以bill_name为key，以True为value的dict
def get_sponsored_and_voted_bills(cosponsors, votes):
    cosponsor_bills = get_sponsored_bills(cosponsors)
    voted_bills = get_voted_bills(votes)
    return {key: True for key in (voted_bills.keys() & cosponsor_bills.keys())}