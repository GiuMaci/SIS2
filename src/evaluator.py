import csv

def computator(filename,fileref):
    """
 
    
    Compares the alignment contained in filename with the reference one contained in fileref. Returns 
    in order recall, precision and the number of matches proposed.
    """
    reference=[]
    confNorm=0
    conf=0
    with open(fileref, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 3:
                continue  # Skip rows that don't have at least two columns
            subj, obj,pred = row[0], row[1],row[2]
            reference.append([row[0],row[1],row[2]])
    with open(filename, mode='r', encoding='utf-8') as file2:
        reader2 = csv.reader(file2)
        matches=0
        lines=0
#        next(reader2)
        for row2 in reader2:
            
            lines+=1
            if len(row2) < 3:
                continue  # Skip rows that don't have at least two columns
            subj, obj,pred = row2[0], row2[1],row2[2]
            confNorm=confNorm+float(row2[3])
            
            
            for k in range(0,len(reference)):
                if ([row2[0],row2[1],row2[2]]==reference[k]) or ([row2[1],row2[0],row2[2]]==reference[k]):
#                    print([row2[0],row2[1],row2[2]],reference[k])
#                    print(matches)
                    matches+=1
                    conf+=float(row2[3])
        
            
    confNorm/=1
    if (matches!=0):
        conf/=matches
    if (len(reference)!=0):
        r=matches/len(reference)
    if (lines!=0):
        p=matches/lines
    return (r,p,lines)
