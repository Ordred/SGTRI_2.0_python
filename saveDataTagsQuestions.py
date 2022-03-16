import json
from numpy import full
import pandas as pd
import secrets
import numpy as np
from objectid import PydanticObjectId

from sgtriAPI import questionAPI, tagAPI

df = pd.read_excel("comma.xlsx", sheet_name="qswithtags")

recs = []

fullTagArray = []

tagNumber = 0

for i, row in df.iterrows():

    if not isinstance(row[2], float):
        tagArray =  row[2].split(';')
    else:
        tagArray = []

    v_values = []

    id = secrets.token_hex(12)

    for j in range(1, 31):
        if row['V'+str(j)] not in ['non']:
            v_values.append(row['V'+str(j)])

    rec = {
        "ID": PydanticObjectId(str(id)), "id": id, "No_Controle" : row[0],"textQuestion": row[1], "vs":v_values
        }

    for tag in tagArray:

        duplicate = False

        for tagFull in fullTagArray:
            if tag == tagFull["name"]:
                duplicate = True
                break

        if duplicate == False:
            questionIDs = []
            questionIDs.append(id)
            tagNumber = tagNumber+1
            recTag = {
                "ID": PydanticObjectId(str(secrets.token_hex(12))), "id": str(secrets.token_hex(12)), "id_int": tagNumber, "name": tag, "questions": questionIDs
                }
            fullTagArray.append(recTag)
        else:
            for tagFull in fullTagArray:
                if tag == tagFull["name"]:
                    questionIDs = tagFull["questions"]
                    questionIDs.append(id)
                    tagFull["questions"] = questionIDs
                    break  

    questionAPI.postFinal(rec)

for tag in fullTagArray:
    tagAPI.postFinal(tag)

for rec in recs:
    print(rec)
    print()

for tag in fullTagArray:
    print(tag)
    print()