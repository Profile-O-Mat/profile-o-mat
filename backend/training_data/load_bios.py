import xml.etree.ElementTree as ET
import os




for filename in os.listdir("mdbs"):
	f = open("mdbs/" + filename, "r").read()
	root = ET.fromstring(f)
	party = root.find("mdbInfo").find("mdbPartei").text.replace("/", "\\")
	o = open("partys/profile_urls/" + party, "a")
	url = root.find("mdbInfo").find("mdbHomepageURL").text
	if url != None and "twitter" in url:
		o.write(url + "\n")
	for child in root.find("mdbInfo").find("mdbSonstigeWebsites").findall("mdbSonstigeWebsite"):
		url = child.find("mdbSonstigeWebsiteURL").text
		if "twitter" in url:
			o.write(url + "\n")
	o.close()