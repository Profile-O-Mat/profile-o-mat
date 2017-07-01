import os
from twitter import *

api = Twitter(auth=OAuth(os.environ['ACCESS_TOKEN_KEY'], os.environ['ACCESS_TOKEN_SECRET'], os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET']))


for fraction in os.listdir("partys/"):
	for account in os.listdir("partys/" + fraction):
		try:
			statuses = api.statuses.user_timeline(screen_name=account, count=200)
			for status in statuses:
				print(fraction + " " + account + ": [" + str(status.id) + "] " + status.text + "\n")

				file = open("partys/" + fraction + "/" + account + "/" + str(status.id) + '.TXT', 'w+')
				file.write(status.text)
				file.close()
		except:
			print("Failed to read profile!")
