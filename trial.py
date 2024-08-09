import json
dic = {}
with open('data.json', 'r') as f:

    dic = json.load(f)

print(dic['initData']['firstPageList']['hotelList'][0]['hotelBasicInfo'].keys())