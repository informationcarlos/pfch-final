# pfch-final
Libraries needed:

Requests (http://docs.python-requests.org/en/latest/)

Beautiful Soup (http://www.crummy.com/software/BeautifulSoup/)

RDFlib (https://github.com/RDFLib/rdflib)

The goal of this project is to perform a preliminary investigation on the quality, thoroughness, and implicit biases found on the semantic web. The focus of my work is DBpedia, a crowd-sourced community effort to extract structured information from Wikipedia and make this information available on the Web (http://dbpedia.org/about). As one of the largest source of structured semantic data on the web, the information found on DBpedia is incredibly important for many LODLAM projects. The investigation focused on particularly subjective properties in the DBpedia ontology: influences. These influence properties were examined for artists specifically in the domain of contemporary art. 

To extract the data for analysis, I wrote a python script that creates a .csv file that is immediately ready to import into Gephi, an open-source software for network visualization and analysis (http://gephi.org/about/). The script first uses Beautiful Soup (http://www.crummy.com/software/BeautifulSoup/) to scrape the Wikipedia page for Contemporary Art to produce a list of Contemporary Art Movements according to Wikipedia. Then, the script navigates to each art movement’s JSON data file in DBpedia and searches for artists who are part of that art movement, and puts their DBpedia URIS in a list. This list of artist URIS is then looped through to filter artists who:

1. Have a DBpedia URI

2. Are people 

3. Have an influence property in their record

These filters are important to only analyze the relationships between people. Once the list of Artists is finalized, they are looped through RDFlib (https://github.com/RDFLib/rdflib), which is a Python library for working with RDF. Each artists’ URI is parsed through RDFlib, and the script searches for the artists that are influenced by and influential to the artist the script is searching through. If an artist is found in an influence property, a test is run to make sure that the match:

1. Has a DBpedia URI

2. Is a person

If these conditions are met, the script writes the “literal” name of each artist to the .csv file. This needs to be done because the script has been dealing with URIs this whole time, which wouldn’t be helpful as labels in the visualizations. After all the data has been written, the script performs one last step to remove all the duplicate rows of data in the .csv file and produces a final .csv to load into Gephi. 


