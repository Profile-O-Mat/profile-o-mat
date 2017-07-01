import os
import json
from twitter import *

api = Twitter(auth=OAuth("881137326726029313-1ZKsBVbZlra9TxjbbOZStjpCX2rFWOJ","Kj71KOy0XGuktCrR2IJcwhQYBp9gabuxMcChhItdNa5Zu", "GBvHlmhvAhaYrLbaK7iIql9mD", 'iftBQQ3LEHwhDwNS5koK6gCi78n1Ak7yvU3DuwZfgoJBHDLV11'))

with open("mdbs_twitter.json", 'r') as f:
    mdbs = json.load(f)
    for mdb in mdbs:
        print(mdb)
        try:
            api.friendships.create(screen_name=mdb, follow=False)
        except Exception as e:
            print(e)

