import xml.etree.ElementTree as ET

racenumlist = ["name"]
i = 0

file = r"C:\Users\Justin\Documents\Orienteering\Rankings\test_results\2018-05-08_BrownPark_results-IOFv3.xml"
# Read file and remove namespaces if they exist (IOF XML v3)
it = ET.iterparse(file)
for _, el in it:
	if '}' in el.tag:
		el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
root = it.root



for ClassResult in root.findall("ClassResult"):
	racenumstr = "race" + str(i + 1)
	racenumlist.append(racenumstr)
	i = i + 1
	print(racenumlist)
