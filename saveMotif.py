import json
from django.test import tag
from numpy import True_, full
import pandas as pd
import secrets
import numpy as np

from questionsAPI import motifAPI

df = pd.read_excel("C:/Users/jonathan.albrecht/Documents/GitHub/SGTRI_2.0_python/motif_edited.xlsx", sheet_name="motif")

motifs = []

tagNumber = 0

for i, row in df.iterrows():

    if not isinstance(row['label motif'], float) and not isinstance(row['label motif'], int):
        labelArray =  row['label motif'].split(',')
    else:
        labelArray = []


    if not isinstance(row['All degrees'], float):
        degreeArray =  row['All degrees'].split(',')
    else:
        degreeArray = []

    if not isinstance(row[10], float):
        glasgow =  True
    else:
        glasgow =  False

    if not isinstance(row[11], float):
        pupilles =  True
    else:
        pupilles =  False

    if not isinstance(row[12], float):
        pouls =  True
    else:
        pouls =  False

    if not isinstance(row[13], float):
        tah =  True
    else:
        tah =  False

    if not isinstance(row[14], float):
        index_de_choc =  True
    else:
        index_de_choc =  False

    if not isinstance(row[15], float):
        fr =  True
    else:
        fr =  False

    if not isinstance(row[16], float):
        spo2 =  True
    else:
        spo2 =  False

    if not isinstance(row[17], float):
        peak_flow =  True
    else:
        peak_flow =  False

    if not isinstance(row[18], float):
        t_c =  True
    else:
        t_c =  False

    if not isinstance(row[19], float):
        glyceme =  True
    else:
        glyceme =  False

    if not isinstance(row[20], float):
        acentonurie =  True
    else:
        acentonurie =  False

    if not isinstance(row[21], float):
        douleurs =  True
    else:
        douleurs =  False

    if not isinstance(row[22], float):
        cyanose =  True
    else:
        cyanose =  False

    conditions = []

    id = str(secrets.token_hex(12))

    for j in range(1, 15):
        if not isinstance(row['Condition '+str(j)], float):
            conditions.append({"condition": row['Condition '+str(j)], "degree": int(row['Degree C'+str(j)])})
            

    rec = {
        "ID": id,"id_int" : row[0], "category": row[1], "labels": labelArray,
        "degrees": degreeArray, "glasgow": glasgow, "pupilles": pupilles,
        "pouls": pouls, "tah": tah, "index_de_choc": index_de_choc, 
        "fr": fr, "spo2": spo2, "peak_flow": peak_flow,
        "t_c": t_c, "glyceme": glyceme, "acetonurie": acentonurie, 
        "douleurs": douleurs, "cyanose": cyanose, "conditions": conditions
        }

    motifAPI.postFinal(rec)

    print(rec)