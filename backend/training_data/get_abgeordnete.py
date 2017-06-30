import requests
import xml.etree.ElementTree as ET

bios = []
r = requests.get("https://www.bundestag.de/xml/mdb/index.xml")
root = ET.fromstring(r.text)
for child in root.find("mdbs").findall("mdb"):
	f = open("mdbs/" + child.find("mdbID").text, "w")
	f.write(requests.get(child.find("mdbInfoXMLURL").text).text)
	f.close()
	print("Wrote: " + child.get("fraktion") + " - " + child.find("mdbName").text + " - " + child.find("mdbID").text)