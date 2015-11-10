import requests
import json
import re
import csv

with open('ULAN performance artists.csv', 'r') as csvfile:
	lines = csv.reader(csvfile)

	for a_line in lines:

		ulanURI = a_line[0]

		artistNAME = a_line[1]

		#compile our pattern
		p = re.compile('[0-9]{9}')


		#search method
		m= p.findall(ulanURI)

	
		for ulanID in m:
			try:

				r = requests.get('http://www.viaf.org/viaf/sourceID/JPG|' +ulanID)
				
				viafURI = requests.get(r.url)
				
				viafURIJSON = viafURI.url + "justlinks-json"
				
				v = requests.get(viafURIJSON)
				
				response = json.loads(v.text)
			
				try:
					for entry in response['Wikipedia']:

						if "en.wikipedia" in entry:

							wikipediaURL = entry


							dbpediaURL = re.sub("en.wikipedia.org/wiki/","dbpedia.org/page/",wikipediaURL)
							dbResource = re.sub('/page/','/resource/',dbpediaURL)

							dbJSON = re.sub('/page/','/data/', dbpediaURL)

							dbJSON = dbJSON + ".json"

							q = requests.get(dbJSON)

							jsonresponse = json.loads(q.text)

							try:

								for data in jsonresponse[dbResource]['http://dbpedia.org/ontology/influenced:']:
									print (artistNAME + ";"+ "is influence of;" + data['value'])
							except:
								pass

							try:

								for data in jsonresponse[dbResource]['http://dbpedia.org/property/influenced']:
									print (artistNAME + ";"+ "is influence of;" + data['value'])
							except:
								pass

							try:

								for data in jsonresponse[dbResource]['http://dbpedia.org/ontology/influencedBy']:
									print (artistNAME + ";"+ "is influenced by;" + data['value'])
							except:
								pass
							try:

								for data in jsonresponse[dbResource]['http://dbpedia.org/property/influencedBy']:
									print (artistNAME + ";"+ "is influenced by;" + data['value'])
							except:
								pass
				except:
					pass
			except:
				pass
				


	

