import os
import pandas as pd
import json

from src.alignment import referenceAlignments as refAl
from src.textExtraction import textExtractor as texEx
from src.evaluator import computator

from src.core import (
    reader, onto_dict, split_by_caps, embedded_dict, myembed,
    matchrelated, topN, remove_special_characters, matcher_of_indexes,
    RTXmatcher, SEMEMBmatcher
)

def load_config(config_file="config.json"):
    script_dir = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(script_dir, config_file)

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def main():
    
    # 1. Load config
    config = load_config("config.json")
    Ks = config.get("Ks", [1,2,3,5,8,10,12,15,18,25])  # fallback if not present
    script_dir = os.path.abspath(os.path.dirname(__file__))

    # ------------------------------------------------------------------------
    # 1. REFERENCE ALIGNMENT CREATION  PHASE
    # ------------------------------------------------------------------------
    alignment_dir = os.path.join(script_dir, "src", "alignment")
    
    # Run the parser in referenceAlignments.py, passing the directory:
    refAl.parser(alignment_dir)

    # Gather .rdf filenames
    rdf_names = []
    for filename in os.listdir(alignment_dir):
        if filename.endswith(".rdf"):
            # e.g. "file1.rdf" -> "file1"
            name_wo_ext = os.path.splitext(filename)[0]
            rdf_names.append(name_wo_ext)
    
    print("List of .rdf files:", rdf_names)

    # ------------------------------------------------------------------------
    # 2. TEXT EXTRACTION FROM RDF PHASE
    # ------------------------------------------------------------------------
    text_extraction_dir = os.path.join(script_dir, "src", "textExtraction")

    for filename in os.listdir(text_extraction_dir):
        filepath = os.path.join(text_extraction_dir, filename)
        if os.path.isfile(filepath) and filename.endswith(".owl"):
            print("File:", filename)
            # Remove the ".owl" extension
            name_wo_ext = filename[:-4]  # or filename.split('.owl')[0]
            print(name_wo_ext)
            texEx.genrelatedtxt(name_wo_ext)
    
    # ------------------------------------------------------------------------
    # 3. CORE/ EMBEDDING AND EVALUATION PHASE
    # ------------------------------------------------------------------------
    # We will store results in a DataFrame
    datas = pd.DataFrame()

    # If your text files are also in "src/textExtraction",
    # define that directory for reading .txt below:
    text_dir = text_extraction_dir

    for al in rdf_names:
        print("Current alignment:", al)
        
        # Suppose your .rdf filenames look like "cmt-ekaw.rdf"
        # so splitting on '-' gives ["cmt", "ekaw"]
        name1, name2 = al.split("-")

        # Build file paths for the text files, e.g. "cmt.txt"
        cmt_text_path = os.path.join(text_dir, f"{name1}.txt")
        ekaw_text_path = os.path.join(text_dir, f"{name2}.txt")

        # Read the .txt into your data structures
        cmt_data = reader(cmt_text_path)
        ekaw_data = reader(ekaw_text_path)

        # Convert them to dictionaries
        cmt_dict = onto_dict(cmt_data)
        ekaw_dict = onto_dict(ekaw_data)

        # Prepare the data for RTX-based embedding
        cmtRTX = []
        ekawRTX = []

        for row in cmt_data:
            text_combined = row[0] + row[1] + row[2]
            text_cleaned = remove_special_characters(text_combined)
            string_splitted = split_by_caps(text_cleaned)
            cmtRTX.append(string_splitted)
        
        for row in ekaw_data:
            text_combined = row[0] + row[1] + row[2]
            text_cleaned = remove_special_characters(text_combined)
            string_splitted = split_by_caps(text_cleaned)
            ekawRTX.append(string_splitted)

        # Get embedded dictionaries
        embedded_dict_cmt = embedded_dict(cmt_dict)
        embedded_dict_ekaw = embedded_dict(ekaw_dict)

        # Create embeddings from your RTX approach
        cmtvec, ekawvec = myembed(cmtRTX, ekawRTX, 0)

        # values of K to test, could be changed to perform more analysis
        Ks = [1, 2, 3, 5, 8, 10, 12, 15, 18, 25]

        # For each K, we do two types of matching: RTXmatcher and SEMEMBmatcher
        for K in Ks:
            print("K =", K)
            # 1) RTX matching
            rtx_csv_path = os.path.join(os.getcwd(), f"{al}.csv")
            RTXmatcher(K, cmt_data, ekaw_data, cmtvec, ekawvec, rtx_csv_path)

            # Compare results
            gold_alignment_path = os.path.join(alignment_dir, f"{al}-referencealignment.csv")
            result = computator(rtx_csv_path, gold_alignment_path)

            # store the Recall
            datas.loc[K, al + "RELTX"] = result[0]
            
            # Remove the temporary CSV
            if os.path.exists(rtx_csv_path):
                os.remove(rtx_csv_path)

            # 2) SEMEMB matching
            sememb_csv_path = os.path.join(os.getcwd(), f"{al}SEMEMB.csv")
            SEMEMBmatcher(K, cmt_data, ekaw_data,
                          embedded_dict_cmt, embedded_dict_ekaw,
                          sememb_csv_path)
            
            result = computator(sememb_csv_path, gold_alignment_path)
            datas.loc[K, al + "SEMEMB"] = result[0]
            
            # Remove the temporary CSV
            if os.path.exists(sememb_csv_path):
                os.remove(sememb_csv_path)

    # Round the DataFrame and save
    datas = datas.round(2)
    datas.to_csv("final_eval_output.csv", index=False)
    print("Final evaluation saved to final_eval_output.csv")

if __name__ == "__main__":
    main()
