import json
import os

mdbs = {}
for fraction in os.listdir("partys/"):
	for account in os.listdir("partys/" + fraction):
		mdbs[account] = fraction.replace("Bündnis 90\\Die Grünen", "b90").replace("Die Linke", "linke").replace("fraktionslos", "erica")

f = open("mdbs_twitter.json", "w")
f.write(json.dumps(mdbs))
f.close()