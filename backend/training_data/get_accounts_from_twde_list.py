import os
import json
import twitter

from load_bios import create

api = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
                  consumer_secret=os.environ['CONSUMER_SECRET'],
                  access_token_key=os.environ['ACCESS_TOKEN_KEY'],
                  access_token_secret=os.environ['ACCESS_TOKEN_SECRET'])

statuses = api.GetListMembers(list_id=67426883)

with open("mdbs.json", 'r') as f:
    mdbs = json.load(f)

parties = ('CDU', 'CSU', 'Die Linke', 'SPD', 'Bündnis 90\\Die Grünen', 'fraktionslos')

for s in statuses:
    party = ""
    print(s.screen_name, s.name)
    for key in mdbs.keys():
        if key in s.name or s.name in key:
            party = mdbs[key]
    if not party:
        print("skipped " + s.name)
        continue
        # i = int(input("Party: "))
        # party = parties[i]
    print(party)
    create(party, "https://twitter.com/"+s.screen_name)
