import os
import twitter

api = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
                  consumer_secret=os.environ['CONSUMER_SECRET'],
                  access_token_key=os.environ['ACCESS_TOKEN_KEY'],
                  access_token_secret=os.environ['ACCESS_TOKEN_SECRET'])


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
