import json
from django.test import tag
from numpy import full
import pandas as pd
import secrets
import numpy as np

from questionsAPI import questionAPI, tagAPI

df = pd.read_excel("C:/Users/jonathan.albrecht/Documents/GitHub/SGTRI_2.0_python/comma.xlsx", sheet_name="pilkku")

recs = []

fullTagArray = []

tagNumber = 0

for i, row in df.iterrows():

    if not isinstance(row[3], float):
        tagArray =  row[3].split(';')
    else:
        tagArray = []

    v_values = []

    id = str(secrets.token_hex(12))

    for j in range(1, 31):
        if row['V'+str(j)] not in ['non']:
            v_values.append(row['V'+str(j)])

    rec = {
        "ID": id,"No_Controle" : row[1],"textQuestion": row[2], "vs":v_values
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
                "ID": str(secrets.token_hex(12)), "id_int": tagNumber, "name": tag, "questions": questionIDs
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