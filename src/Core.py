import torch
import numpy as np
import gensim.downloader as api
import csv
import re

def findindex(onto,concept):
    for i in range(0,len(onto)):
        if onto[i][0]==concept:
            return(i)
# reurns concept index and concept in ontology
def findconcept(onto,concept):
    for i in range(0,len(onto)):
        if onto[i][0]==concept:
            return(i,onto[i])

# Computes the cosine similarity between two vectors.

def cosine_similarity(vec_a, vec_b): #COS SIMILARITY
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if(norm_a !=0 and norm_b!=0):
        return dot_product / (norm_a * norm_b)
    else:
        return 0

#Returns the topN concept from list_of_lists according the given parameter

def topN(list_of_lists, N):
    # Sort the list of lists based on the first element of each sublist in descending order
    sorted_list = sorted(list_of_lists, key=lambda x: x[0], reverse=True)
    
    # Get the top N elements
    top_n = sorted_list[:N]
    
    return top_n


#splits the text in camelCase
def split_by_caps(input_string):
    # Using regular expression to split the string at capital letters
    words = re.findall('[^A-Z]+|[A-Z][^A-Z]*', input_string)
    # Joining the words with spaces
    return ' '.join(words)

#removes the characters list

def remove_special_characters(text, characters="-_"):
    # Create a regular expression pattern that includes all characters to be removed
    regex_pattern = f"[{re.escape(characters)}]"
    # Replace the characters with an empty string
    cleaned_text = re.sub(regex_pattern, "", text)
    return cleaned_text

#reads the file and returns the content in a list of lists
def reader(file_path): 

    LISTONA=[]
    listaout=[]
# Open the file using 'with' statement
    with open(file_path, 'r') as file:
    # Read and print each line
        for line in file:
            LISTONA.append((line.strip().split(',',2))) # .strip() removes leading/trailing whitespace, including newlines
#            listaout=LISTONA.split(',', 1)
    return(LISTONA)

 #takes as an input the list in reader. Creates a list of dictionaries. Each concept in onto has it's own 
    # dictionary, with ID=local name of the class, and then a list of keys that are the properties present for that concept
    # the values are the objects for that property
    
def onto_dict(onto):
    list_of_dictionary=[]
    for i in range(0,len(onto)):
        diz={}
        diz['ID']=split_by_caps(remove_special_characters(onto[i][0]))
        text_to_dictz=onto[i][2].split(';')
        if(onto[i][2]==''):
            list_of_dictionary.append({str(i):''})
            continue
        for k in text_to_dictz:
            diz[split_by_caps(k.split(':')[0])]=split_by_caps(k.split(':')[1])
        list_of_dictionary.append(diz)
    return(list_of_dictionary)

#from the onto_dict obtained list of dictionaries is created another list of dictionaries. Now the values of the keys are the 
# embeddings obtained with the embeddere function
def embedded_dict(list_of_dict):
    embedded_dictionaries=[]
    for concept in list_of_dict:
        diz2={}
        for i in concept.keys():
            diz2[i]=embedder(concept[i],model)
        embedded_dictionaries.append(diz2)
    return(embedded_dictionaries)
