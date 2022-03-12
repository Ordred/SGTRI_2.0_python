import json
from django.test import tag
from numpy import full
import pandas as pd

df = pd.read_excel("C:/Users/jonathan.albrecht/Documents/GitHub/SGTRI_2.0_python/data/xlsxtojson/comma.xlsx", sheet_name="pilkku")

recs = []

fullTagArray = []

tagNumber = 0

for i, row in df.iterrows():

    if not isinstance(row[3], float):
        tagArray =  row[3].split(';')
    else:
        tagArray = []

    v_values = []

    for j in range(1, 31):
        if row['V'+str(j)] not in ['non']:
            v_values.append(row['V'+str(j)])

    rec = {
        "ID": row[0],"No_Controle" : row[1],"textQuestion": row[2], "V-Values":v_values
        }

    for tag in tagArray:

        duplicate = False

        for tagFull in fullTagArray:
            if tag == tagFull["name"]:
                duplicate = True
                break

        if duplicate == False:
            questionIDs = []
            questionIDs.append(row[0])
            tagNumber = tagNumber+1
            recTag = {
                "ID": tagNumber, "name": tag, "questions": questionIDs
                }
            fullTagArray.append(recTag)
        else:
            for tagFull in fullTagArray:
                if tag == tagFull["name"]:
                    questionIDs = tagFull["questions"]
                    questionIDs.append(row[0])
                    tagFull["questions"] = questionIDs
                    break                
    recs.append(rec)
    

for tag in fullTagArray:
    print(tag)
    print()

for rec in recs:
    print(rec)
    print()