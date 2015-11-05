import requests
import json
import re

perfArt = 'http://dbpedia.org/data/Performance_art.json'
r = requests.get(perfArt)

response = json.loads(r.text)

for entry in response:
	entry = str(entry)
	reg = re.sub('/resource/', '/data/', entry)
	try:
		s = requests.get(reg + ".json")
		info = json.loads(s.text)
	except:
		pass
	try:
		for agent in info[entry]['http://www.w3.org/1999/02/22-rdf-syntax-ns#type']:
			if "http://schema.org/Person" in agent['value']:
				perfArtist = entry
				perfArtist = str(perfArtist)
				regex = re.sub('/resource/', '/data/', perfArtist)
				try:
					t = requests.get(regex + ".json")
					artistInfo = json.loads(t.text)
				except:
					pass
				try:
					for data in artistInfo[perfArtist]:
						if "influenced" in data:
							print (perfArtist)
				except:
					pass

	except:
		pass
	

