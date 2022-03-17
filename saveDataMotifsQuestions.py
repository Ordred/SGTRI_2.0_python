import pandas as pd
import secrets
import numpy as np
from objectid import PydanticObjectId
from sgtriAPI import questionAPI, motifquestionAPI

df = pd.read_excel("comma.xlsx", sheet_name="qswithmotif")
recs = []
fullMotifArray = []
id = 0

for i, row in df.iterrows():

    if not isinstance(row[2], float):
        rawMotif =  row[2]
        mtf = str(rawMotif)
        mtf = mtf.split("/")
        motifArray = [int(i) for i in mtf]
    else:
        motifArray = []

    v_values = []

    id = id+1

    for j in range(1, 31):
        if row['V'+str(j)] not in ['non', '']:
            v_values.append(row['V'+str(j)])

    rec = {
        "ID": PydanticObjectId(secrets.token_hex(12)), "id_int": id, "No_Controle" : row[0],"textQuestion": row[1], "vs":v_values
        }


    for motif in motifArray:
        duplicate = False

        for motifFull in fullMotifArray:
            if motif == motifFull["idMotif"]:
                duplicate = True
                break

        if duplicate == False:
            questionIDs = []
            questionIDs.append(id)
            recMotif = {
                "ID": PydanticObjectId(secrets.token_hex(12)), "idMotif": motif, "questions": questionIDs
                }
            fullMotifArray.append(recMotif)
        else:
            for motifFull in fullMotifArray:
                if motif == motifFull["idMotif"]:
                    questionIDs = motifFull["questions"]
                    questionIDs.append(id)
                    motifFull["questions"] = questionIDs
                    break  
        questionAPI.postFinal(rec)
    
fullMotifArray = sorted(fullMotifArray, key=lambda x: x["idMotif"])   

for motif in fullMotifArray:
    motifquestionAPI.postFinal(motif)

