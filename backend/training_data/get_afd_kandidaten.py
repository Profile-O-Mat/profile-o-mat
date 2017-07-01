import os
import twitter

from load_bios import create

api = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
                  consumer_secret=os.environ['CONSUMER_SECRET'],
                  access_token_key=os.environ['ACCESS_TOKEN_KEY'],
                  access_token_secret=os.environ['ACCESS_TOKEN_SECRET'])

accounts = api.GetListMembers(list_id=857844352185503748)

for account in accounts:
    print(account.screen_name)
    create("AfD", "https://twitter.com/" + account.screen_name)
