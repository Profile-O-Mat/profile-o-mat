import os
import json
from twitter import *

from load_bios import create

api = Twitter(auth=OAuth(os.environ['ACCESS_TOKEN_KEY'], os.environ['ACCESS_TOKEN_SECRET'], os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET']))

statuses = api.lists.members(list_id=67426883)

with open("mdbs.json", 'r') as f:
    mdbs = json.load(f)

parties = ('CDU', 'CSU', 'Die Linke', 'SPD', 'Bündnis 90\\Die Grünen', 'fraktionslos')

for s in statuses["users"]:
    party = ""
    print(s['screen_name'], s['name'])
    for key in mdbs.keys():
        if key in s['screen_name'] or s['name'] in key:
            party = mdbs[key]
    if not party:
        print("skipped " + s['name'])
        continue
        # i = int(input("Party: "))
        # party = parties[i]
    print(party)
    create(party, "https://twitter.com/"+s['screen_name'])
