import xml.etree.ElementTree as ET
import os
import json


def create(party, url):
	if not os.path.isdir("partys/" + party):
		os.mkdir("partys/" + party)
	if not os.path.isdir("partys/" + party + "/" + url.split("/")[-1].split("?")[0]):
		os.mkdir("partys/" + party + "/" + url.split("/")[-1].split("?")[0])

mdbs = {}


if __name__ == "__main__":
	for filename in os.listdir("mdbs"):
		f = open("mdbs/" + filename, "r").read()
		root = ET.fromstring(f)
		party = root.find("mdbInfo").find("mdbPartei").text.replace("/", "\\")
		name = root.find("mdbInfo").find("mdbVorname").text + " " + root.find("mdbInfo").find("mdbZuname").text
		mdbs[name] = party
		url = root.find("mdbInfo").find("mdbHomepageURL").text
		if url != None and "twitter" in url:
			print(name)
			create(party, url)
		for child in root.find("mdbInfo").find("mdbSonstigeWebsites").findall("mdbSonstigeWebsite"):
			url = child.find("mdbSonstigeWebsiteURL").text
			if "twitter" in url:
				print(name)
				create(party, url)

	f = open("mdbs.json", "w")
	f.write(json.dumps(mdbs))
	f.close()
