import os
import twitter

from load_bios import create

api = twitter.Api(consumer_key="EOrXKkxg0XzFzlFOTA3jDAs4f",
                  consumer_secret='MOpd38qVPPL2okboPfRh8zydfLRFmy3mulB5LhQv1xKKsfMHRh',
                  access_token_key="388252133-aVIPGzoy8D19TP4QdBBhV0zlOMlmwcoSOt760KRs",
                  access_token_secret="obs8ggbMMlULwijO3PCAhqDRn8joUssOEsaQHyi5uF10r")

accounts = api.GetListMembers(list_id=857844352185503748)

for account in accounts:
    print(account.screen_name)
    create("AfD", "https://twitter.com/" + account.screen_name)
