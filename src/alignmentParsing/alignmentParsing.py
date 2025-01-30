import rdflib
import csv
import os

def remove_base_uri(input_string):
    parts = input_string.split(", ")  # Split the string at each comma and space
    cleaned_parts = []
    for part in parts:
        # Split each part at '#' and take the second part
        cleaned_part = part.split("#")[-1]
        cleaned_parts.append(cleaned_part)
    return ", ".join(cleaned_parts)

# Set the directory path where the files are stored
directory_path = os.getcwd()

# List to hold the names of .rdf files
names = []

# Loop through each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.rdf'):
        names.append(filename.split('.')[0])

# Print the list of .rdf files
print("List of .rdf files:", names)

#names=['cmt-iasted','cmt-edas']
# Load the RDF file



predicate1 = "http://knowledgeweb.semanticweb.org/heterogeneity/alignmententity2"
predicate2 = "http://knowledgeweb.semanticweb.org/heterogeneity/alignmententity1"

# SPARQL query to select all objects for the given predicate
query = f"""
    SELECT ?object1 ?object2
    WHERE {{
        ?subject <{predicate1}> ?object1.
        ?subject <{predicate2}> ?object2. 
        
    }}
"""
for i in names:
    g = rdflib.Graph()
   

    try:
        g.parse(i+'.rdf', format="xml")
    except Exception as e:
        print(f"An error occurred: {e}")
        pass

#    g.parse(i+'.rdf', format='xml')  # Replace with your RDF file path
# Execute the query
    qres = g.query(query)

    filename = str(i)+'referencealignment.csv'

# Open the file in write mode
    with open(filename, 'w', newline='') as csvfile:
    # Create a writer object from csv module
        csvwriter = csv.writer(csvfile)
    
    # Write each row to the CSV file
        for row in qres:
            csvwriter.writerow([remove_base_uri(row.object1),remove_base_uri(row.object2),'='])

    print(f'CSV file "{filename}" has been created and populated with data row by row.')
