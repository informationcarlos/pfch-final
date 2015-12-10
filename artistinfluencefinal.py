import requests
import json
import re
import csv
from rdflib import Graph, URIRef
import logging
from bs4 import BeautifulSoup

logging.basicConfig()

#open up csv file that we will eventually write to
with open("artistinfluencedataFINAL.csv", "w") as csvfile:
	writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
	#easy way to write headers 
	writer.writerow(["source", "target", "type"])
	pass


###################### Sweet Function Action #################################
# function to check if URI is a Person 
def personcheck(person_uri):

	try:
		#change URI to JSON URI and loads JSON file
		reg = re.sub('/resource/', '/data/', person_uri)
		o = requests.get(reg + ".json")
		person_json = json.loads(o.text)

		#loop through JSON file to find a Person #type property and return True if exists
		for record in person_json[person_uri]['http://www.w3.org/1999/02/22-rdf-syntax-ns#type']:
			if "http://schema.org/Person" in record['value']:
			
				return True
	except:
		return False

# function to find name string of URI
def namecheck(name_uri):

	try:
		#change URI to JSON URI and loads JSON file
		regular = re.sub('/resource/', '/data/', name_uri)
		p = requests.get(regular + ".json")
		person_json = json.loads(p.text)
		
		try:
			#loop through JSON file to find a Label #type property 
			for name in person_json[name_uri]["http://www.w3.org/2000/01/rdf-schema#label"]:
				#if the label is in english, return that name
				if name['lang'] == "en":
					name_label = name['value']
			
					return name_label
		except:
			#if record doesn't have Label #type property, regex the name from the URI
			namehttpremoved = re.sub("http://dbpedia.org/resource/","", name_uri)
			name_label = re.sub("_", " ", namehttpremoved)
			
			return name_label
	except:
		pass
	


#function to find influences of Artists in 20th Century art movements
def artistinfluence(art_movement): 
	
	#open CSV file to append data in each loop
	with open("artistinfluencedataFINAL.csv", "a") as csvfile:

		
		#set variable to none to prevent errors later on
		# artistswithinfluences = None
		
		#set CSV writer parameters
		writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)


		#need to change art movement dbpedia URI to JSON dump and load it up
		movement_json = re.sub('/page/', '/data/', art_movement)
		q = requests.get(movement_json + ".json")
		response = json.loads(q.text)


		#empty list to store artists with influences in their dbpedia records
		artistswithinfluences = []

		#loop through the art movement JSON to find artists of art movement
		for entry in response:
	
			
			#filter to find other DBPEDIA resources who are most likely artists
			if "http://dbpedia.org/resource/" in entry:
			
				
				#make each filtered entry an artist URI variable
				artist_URI = entry
				
				#change artist URI to JSON dump and load it up
				regex = re.sub('/resource/', '/data/', artist_URI)
				t = requests.get(regex + ".json")
				artistInfo = json.loads(t.text)

				#check entire JSON for the string "/influence" to filter out artist records with influence properties
				if "/influence" in str(artistInfo):

					#run personcheck on artist URIs with influences to make sure they are people 
					if personcheck(artist_URI) == True:

						#store artist URIs with influences in a variable
						artist_URI = str(artist_URI)
						artistswithinfluences.append(artist_URI) 
		
		#loop through artists with influences to find influences and write to CSV			
		for artist in artistswithinfluences:

			#just to know where the loop is 
			print (artist + " " + art_movement)
				
			try:

				#pass artist through RDF graph and parse record
				g = Graph()
				result = g.parse(artist)

				#loop through graph to find objects of influence predicate
				for stmt in g.subject_objects(URIRef("http://dbpedia.org/property/influencedBy")):
					
					subject_URI1 = str(stmt[0])
					object_URI1 = str(stmt [1])

					
						
					
					#I only want to see influences between PEOPLE, so run personcheck on objects
					if personcheck(object_URI1) == True:

						#run namecheck on subject and object to get name literals
						objectlabel1 = namecheck(object_URI1)
						subjectlabel1 = namecheck(subject_URI1)

						#write to csv
						writer.writerow([objectlabel1, subjectlabel1, "directed"])
					
					else:
						pass
					
				
				
		
				for stuff in g.subject_objects(URIRef("http://dbpedia.org/ontology/influencedBy")):
					subject_URI2 = str(stuff[0])
					object_URI2 = str(stuff [1])
					
					
					#prevent duplicate influence entries
					if object_URI1 == object_URI2:
						pass
					
					else:

						if personcheck(object_URI2) == True: 
							#run namecheck on subject and object to get name literals
							objectlabel2 = namecheck(object_URI2)
							subjectlabel2 = namecheck(subject_URI2)
							

							#write to csv
							writer.writerow([ objectlabel2, subjectlabel2, "directed"])
						
						else:
							pass
					

				for more in g.subject_objects(URIRef("http://dbpedia.org/ontology/influenced")):
					subject_URI3 = str(more[0])
					object_URI3 = str(more[1])
					

					
					if personcheck(object_URI3) == True: 
						#run namecheck on subject and object to get name literals
						objectlabel3 = namecheck(object_URI3)
						subjectlabel3 = namecheck(subject_URI3)
						
						
						#write to csv
						writer.writerow([subjectlabel3, objectlabel3, "directed"])
					
					else:
						pass
					
					
			
				for wow in g.subject_objects(URIRef("http://dbpedia.org/property/influenced")):
					subject_URI4 = str(wow[0])
					object_URI4 = str(wow[1])
					
					
					if object_URI3 == object_URI4:
						pass
					
					else:

						if personcheck(object_URI4) == True: 
							#run namecheck on subject and object to get name literals
							objectlabel4 = namecheck(object_URI4)
							subjectlabel4 = namecheck(subject_URI4)
							
							
							#write to csv
							writer.writerow([subjectlabel4, objectlabel4, "directed"])
						
						else:
							pass

			except:
				pass		

############################################Web Scrape################################################
#wikipedia page with contemporary art movement links
url = "https://en.wikipedia.org/wiki/Contemporary_art"

#lets ask requests to get that page
object_page = requests.get(url)

html = object_page.text

soup = BeautifulSoup(html, "html.parser")	

#need to find the table which houses our links
column_one = soup.find_all("table", attrs = {"cellpadding":"0"})

#create empty list to store eventual art movement links
art_movements = []

#find art movements and regex to their dbpedia URI and store in list
for link in column_one:
	for item in link('li'):
		short_url = item.find('a')["href"]

		#takes wiki markdown and changes to dbpedia.org/resource 
		dbpedia_uri_wrong = re.sub("/wiki/","http://dbpedia.org/resource/",short_url)
		
		#since the initial dbpedia uri is sometimes in the wrong case, need to request and get the actual URI
		#rdflib is REALLY picky about case 		
		o = requests.get(dbpedia_uri_wrong)
		dbpedia_uri = o.url
		art_movements.append(dbpedia_uri)


#######################################Where the fun begins#######################
# loop movements through artist influence function
for movement in art_movements:
	
	#just to see the art movements to be fed
	print (movement)

	#run the function!
	artistinfluence(movement)





#after its all said and done, remove duplicate rows
with open("artistinfluencedataFINAL.csv", "r") as in_file, open('artistinfluencedataNODUPLICATES.csv','w') as out_file:
    seen = set() 
    for line in in_file:
        if line in seen: continue # skip duplicate

        seen.add(line)
        out_file.write(line)
