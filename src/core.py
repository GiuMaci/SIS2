import torch
import numpy as np
import gensim.downloader as api
import csv
import re
from src.embeddings import Embeddings

import json

def load_config(path_to_config):
    with open(path_to_config, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    return config_data

model_choice=load_config("/home/serverKB/SIS/config.json")['model_choice']
embedder = Embeddings(model_name=model_choice)  # Create an instance of Embeddings

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
            diz2[i]=embedder.embed(concept[i])
        embedded_dictionaries.append(diz2)
    return(embedded_dictionaries)
    
def myembed(onto1,onto2,index): #TI MANDA I  MIGLIORI CONCETTI FRA TESEO E EUROVOC  #index è il parametro dei due
    onto1vec=[]
    onto2vec=[]

    for i in range(0,len(onto1)):
        onto1vec.append(embedder.embed(onto1[i][index]))
    for i in range(0,len(onto2)):
        onto2vec.append(embedder.embed(onto2[i][index]))
    return(onto1vec,onto2vec)

def matcher_of_indexes(onto1,onto2,embedded_dict_onto1,embedded_dict_onto2,i,indexes):
    Listof=[]
    for j in indexes:
        sim=0
        Norm=0
        if(onto1[i][1]==onto2[j][1]) or (onto1[i][1]!=onto2[j][1]) : #this can be changed if one wants to match same types
            for arrival_key in embedded_dict_onto2[j].keys():
                    for start_key in embedded_dict_onto1[i].keys():
                        if arrival_key==start_key:
                            Norm+=1 #len(ekaw_dict[index-1][arrival_key])
                            sim+=cosine_similarity(embedded_dict_onto1[i][start_key],embedded_dict_onto2[j][arrival_key])
#        if(sim!=0):
#            if (Norm!=0):
#                sim/=Norm
            sim/=len(embedded_dict_onto1[i].keys())
            Listof.append([sim,onto1[i][0],onto2[j][0]])
        else:
            continue
    return(Listof)
# this function takes the two ontologies and the embeddings and returns a List of the shape 
# [<similarity>,conceptOtarget,conceptOsource. The concept in source ontology to be matched is indexed with i. The concepts
# in target ontology are indexed with the list indexes. If you lanuch it with len(otarget) you try the match on all the
# target ontology concepts.

def matchrelated(onto1,onto2,onto1vec,onto2vec,i,indexes):
    Listof=[]
    for j in indexes:
        sim=0
        Norm=0
        if(onto1[i][1]==onto2[j][1]) or (onto1[i][1]!=onto2[j][1]) : #This line is for the type compatibility control         
            sim=cosine_similarity(onto1vec[i],onto2vec[j])            
            Listof.append([sim,onto1[i][0],onto2[j][0]])
        else:
            continue
    return(Listof)

#THIS FUNCTION TAKES the two ontologies and matches them with the RTX approach. For the names cmt is always the source ontology
# while ekaw is always the target ontology. K is the parameter in the k-neighbors. As imput there are the text list and the
#  embeddings as said. No confidence score is extracted the 1,1 are put jus as a convention, but can be later changed with the 
# confidence scores computed in matchrelated.

def RTXmatcher(K,cmt,ekaw,cmtvec,ekawvec,fileout):
    possiblematches=[]
    indexes=[]
    with open(fileout, mode='w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for i in range(0,len(cmt)):
            Listof=matchrelated(cmt,ekaw,cmtvec,ekawvec,i,range(0,len(ekaw)))
            possiblematches=topN(Listof,K)
            if (possiblematches==[]):
                continue
            else:
                for k in range(0,K):
                    writer.writerow([possiblematches[k][1],possiblematches[k][2],'=','1','1'])
#THIS FUNCTION TAKES the two ontologies and matches them with the SEMEMB approach. For the names cmt is always the source ontology
# while ekaw is always the target ontology. K is the parameter in the k-neighbors. As imput there are the text list and the
#  dictionary embeddings computed nefore. No confidence score is extracted the 1,1 are put just as a convention, but can be
# later changed with the  confidence scores computed in matchrelated.

def SEMEMBmatcher(K,cmt,ekaw,embedded_dict_cmt,embedded_dict_ekaw,fileout):
    possiblematches=[]
    indexes=[]
    with open(fileout, mode='w', encoding='utf-8') as file:
        writer = csv.writer(file)
        for i in range(0,len(cmt)):
            Listof=matcher_of_indexes(cmt,ekaw,embedded_dict_cmt,embedded_dict_ekaw,i,range(0,len(ekaw)))
            possiblematches=topN(Listof,K)
            if (possiblematches==[]):
                continue
            else:
                for k in range(0,K):
                    writer.writerow([possiblematches[k][1],possiblematches[k][2],'=','1','1'])
        
    
