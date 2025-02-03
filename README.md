# Semantic Informed Similarity for Ontology Alignment
Here you find the code used for the paperSIS: Leveraging Semantically-Informed Similarity of Text Embeddings for Enhanced Ontology Alignment.

# config
In config.json you can choose the embedding model (glove or sbert) and the Ks in the k-neighbor search  for which the analysis is carried out.

# Output
Is given as a csv-dataframe (final_eval_output.csv) in which for every alignment in the conference track results are evaluated at different k (each row). The results
are always for the SIS method (SEMEMB column) and the baseline (RELTX column.)

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

# core
Here are stored the functions that perform the most important steps of SIS method.

# embeddings
Here there is the class that defines the two possible type of embeddings: GloVe or SBERT.

# evaluator

Performs the evaluation comparing the alignment obtained and stored in filename with the reference alignment contained in fileref. Returns 
in order recall, precision and the number of matches proposed.



