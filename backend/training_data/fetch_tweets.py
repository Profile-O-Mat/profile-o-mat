import os

for fraction in os.listdir("partys/"):
	for account in os.listdir("partys/" + fraction):
		print(fraction + " " + account)
