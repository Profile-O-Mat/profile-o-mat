import os
import json
import twitter

from load_bios import create

api = twitter.Api(consumer_key="EOrXKkxg0XzFzlFOTA3jDAs4f",
                  consumer_secret='MOpd38qVPPL2okboPfRh8zydfLRFmy3mulB5LhQv1xKKsfMHRh',
                  access_token_key="388252133-aVIPGzoy8D19TP4QdBBhV0zlOMlmwcoSOt760KRs",
                  access_token_secret="obs8ggbMMlULwijO3PCAhqDRn8joUssOEsaQHyi5uF10r")

statuses = api.GetListMembers(list_id=67426883)

with open("mdbs.json", 'r') as f:
    mdbs = json.load(f)

parties = ('CDU', 'CSU', 'Die Linke', 'SPD', 'Bündnis 90\\Die Grünen', 'fraktionslos')

for s in statuses:
    print(s.screen_name, s.name, "\n", s.description)
    print(parties)
    for key in mdbs.keys():
        if s.name in key:
            party = mdbs[key]
    if not party:
        i = int(input("Party: "))
        party = parties[i]
    create(party, "https://twitter.com/"+s.screen_name)
