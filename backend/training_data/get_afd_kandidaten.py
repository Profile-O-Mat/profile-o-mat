import os
from twitter import *

from load_bios import create

api = Twitter(auth=OAuth(os.environ['ACCESS_TOKEN_KEY'], os.environ['ACCESS_TOKEN_SECRET'], os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET']))

accounts = api.lists.members(list_id=857844352185503748)

for account in accounts['users']:
    print(account['screen_name'])
    create("AfD", "https://twitter.com/" + account['screen_name'])
