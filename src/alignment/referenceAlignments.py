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

def parser(directory_path=None):
    # If no directory is given, default to current working directory
    if directory_path is None:
        directory_path = os.getcwd()

# List to hold the names of .rdf files
    names = []

# Loop through each file in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.rdf'):
            names.append(filename.split('.')[0])

# Print the list of .rdf files
    print("List of .rdf files:", names)
    
     # Define predicates
    predicate1 = "http://knowledgeweb.semanticweb.org/heterogeneity/alignmententity2"
    predicate2 = "http://knowledgeweb.semanticweb.org/heterogeneity/alignmententity1"

    # Define the SPARQL query
    # Make sure it's syntactically complete
    query = f"""
        SELECT ?object1 ?object2
        WHERE {{
            ?subject <{predicate1}> ?object1 .
            ?subject <{predicate2}> ?object2 .
        }}
    """

    # Gather all .rdf files in the specified directory
    rdf_files = [f for f in os.listdir(directory_path) if f.endswith('.rdf')]
    print("Found RDF files:", rdf_files)

    # Process each RDF file
    for rdf_file in rdf_files:
        # Build the full path to the file
        rdf_full_path = os.path.join(directory_path, rdf_file)
        
        # Create a fresh Graph for each file
        g = rdflib.Graph()
        try:
            # Parse the RDF file (assuming XML format; adjust if needed)
            g.parse(rdf_full_path, format="xml")
        except Exception as e:
            print(f"An error occurred while parsing {rdf_file}: {e}")
            # Skip to the next file
            continue

        # Run the SPARQL query
        qres = g.query(query)

        # Create a CSV filename based on the RDF file name
        # e.g., "myfile.rdf" -> "myfile-referencealignment.csv"
        base_name = os.path.splitext(rdf_file)[0]
        csv_filename = f"{base_name}-referencealignment.csv"

        # Write the query results to CSV
        csv_full_path = os.path.join(directory_path, csv_filename)
        with open(csv_full_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            
            # Each row in qres is a tuple of bound variables (object1, object2)
            for row in qres:
                # row.object1 and row.object2 are rdflib.term.URIRef or Literal
                # Use your remove_base_uri() or other logic to clean them up
                object1_clean = remove_base_uri(str(row.object1))
                object2_clean = remove_base_uri(str(row.object2))
                
                # Example: write [object1, object2, '='] to each row
                csvwriter.writerow([object1_clean, object2_clean, '='])

        print(f'CSV file "{csv_full_path}" has been created and populated.')

    print("Parsing completed.")