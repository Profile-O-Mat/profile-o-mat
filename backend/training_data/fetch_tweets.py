import os
import twitter

api = twitter.Api(consumer_key="EOrXKkxg0XzFzlFOTA3jDAs4f",
                  	consumer_secret='MOpd38qVPPL2okboPfRh8zydfLRFmy3mulB5LhQv1xKKsfMHRh',
                  	access_token_key="388252133-aVIPGzoy8D19TP4QdBBhV0zlOMlmwcoSOt760KRs",
                  	access_token_secret="obs8ggbMMlULwijO3PCAhqDRn8joUssOEsaQHyi5uF10r")



for fraction in os.listdir("partys/"):
	for account in os.listdir("partys/" + fraction):
		try:
			statuses = api.GetUserTimeline(screen_name=account, count=200)
			for status in statuses:
				print(fraction + " " + account + ": [" + str(status.id) + "] " + status.text + "\n")

				file = open("partys/" + fraction + "/" + account + "/" + str(status.id) + '.TXT', 'w+')
				file.write(status.text)
				file.close()
		except:
			print("Failed to read profile!")
			
