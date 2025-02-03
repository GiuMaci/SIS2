from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS,OWL
import rdflib
import os

def genrelatedtxt2(ontoname,formato="application/rdf+xml"):
    g = Graph()
    filename=ontoname+".owl"
    fileres=ontoname+".txt"
    g.parse(filename, format=formato)
    # Extract the classes
    entities = set(g.subjects(RDF.type, OWL.Class)) | set(g.subjects(RDF.type, OWL.ObjectProperty)) | set(g.subjects(RDF.type, OWL.DatatypeProperty))

    with open(fileres, 'w') as fileout:
        testo=[]
        for class_uri in entities:
            reltxt = extract_predicates_and_objects(g, class_uri)
            formatted_output=format_results(reltxt)
            tipo=get_type_of_uri(g, class_uri)
#            testo.append(triples_to_plain_text(a))
            fileout.write("{}, {}, {}  \n".format(remove_base_uri(class_uri),tipo,formatted_output))
    
def genrelatedtxt(ontoname, formato="application/rdf+xml"):
    # Get the absolute path to the current directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the correct path to the input and output files
    filename = os.path.join(script_dir, ontoname + ".owl")  # .owl file in the same directory
    fileres = os.path.join(script_dir, ontoname.lower() + ".txt")  # Output file

    g = Graph()
    g.parse(filename, format=formato)  # Load ontology file

    # Extract classes, properties, and other entities
    entities = set(g.subjects(RDF.type, OWL.Class)) | set(g.subjects(RDF.type, OWL.ObjectProperty)) | set(g.subjects(RDF.type, OWL.DatatypeProperty))

    with open(fileres, 'w') as fileout:
        for class_uri in entities:
            reltxt = extract_predicates_and_objects(g, class_uri)
            formatted_output = format_results(reltxt)
            tipo = get_type_of_uri(g, class_uri)

            fileout.write("{}, {}, {}\n".format(remove_base_uri(class_uri), tipo, formatted_output))

    print(f"Generated related text file: {fileres}")
def remove_base_uri(input_string):
    parts = input_string.split(", ")  # Split the string at each comma and space
    cleaned_parts = []
    for part in parts:
        # Split each part at '#' and take the second part
        cleaned_part = part.split("#")[-1]
        cleaned_parts.append(cleaned_part)
    return ", ".join(cleaned_parts)
  
def get_type_of_uri(rdf_graph, uri):
    """
    Given an RDF graph and a URI, this function checks the RDF type of the URI and returns its name.
    
    Parameters:
    rdf_graph (Graph): An rdflib Graph object containing RDF data.
    uri (str): The URI as a string whose type is to be determined.

    Returns:
    str: The name of the RDF type of the given URI, or 'Unknown' if not found.
    """
    # Convert the string URI to an rdflib URIRef object
    uri_ref = URIRef(uri)
    
    # Query the graph for the RDF type of the given URI
    for _, _, rdf_type in rdf_graph.triples((uri_ref, RDF.type, None)):
        if rdf_type:
            return rdf_type.split('#')[-1]  # Returning the local name of the type

    # Return 'Unknown' if no type was found
    return "Unknown"

def extract_predicates_and_objects(graph, uri):
    uri_ref = URIRef(uri)
    results = {}

    for predicate, obj in graph.predicate_objects(subject=uri_ref):
        pred_str = str(remove_base_uri(predicate))
        if isinstance(obj, URIRef):
            obj_str = str(remove_base_uri(obj))
        else:
            obj_str = str(obj)

        if pred_str not in results:
            results[pred_str] = []
        results[pred_str].append(obj_str)
    return results

def format_results(results):
    formatted_output = []
    for predicate, objects in results.items():
        cleaned_objects = [obj.replace('\n', '') for obj in objects]
        formatted_output.append(f"{predicate}: {','.join(cleaned_objects)}")
    return "; ".join(formatted_output)


