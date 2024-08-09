import json
dic = {}
with open('data3.json', 'r') as f:

    dic = json.load(f)

for x in dic['initData']['htlsData']['inboundCities']:
    print(x['name'], x['id'])