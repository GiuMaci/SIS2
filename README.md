# Semantic Informed Similarity for Ontology Alignment
Here you find the code used for the paperSIS: Leveraging Semantically-Informed Similarity of Text Embeddings for Enhanced Ontology Alignment.

# alignment
Takes the rdf alignment files from OAEI conference track (ra1) https://oaei.ontologymatching.org/2023/conference/data/reference-alignment.zip
and transform them in .csv files that the evaluator uses to calculate recall. In Conference-ConfOf.rdf file there is an error that has been fixed 
to ensure the parsing works well.

# textExtractor
Extracts relvant information from a .owl file and puts it in a .txt format with this given structure 

Type of the .txt format: 

local_name, type, predicate1: obj1, ... , objN; .... ; predicateN: obj1, ..., objN \n

example: 

||Social_Event, Class, type: Class; disjointWith: Contributed_Talk,Conference,Invited_Talk,Track,Workshop,Tutorial; subClassOf: Event. ||

.owl files are at: https://oaei.ontologymatching.org/2023/conference/index.html

# Core
Here are stored the functions that perform the most important steps of SIS method.
# Evaluator

Performs the evaluation comparing the alignment obtained from SemEmbCore(SBERT or GloVe) and stored in filename with the reference alignment contained in fileref. Returns 
in order recall, precision and the number of matches proposed.



