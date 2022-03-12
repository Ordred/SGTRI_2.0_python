import json
import pandas as pd

df = pd.read_excel("C:/Users/jonathan.albrecht/Documents/GitHub/SGTRI_2.0_python/data/xlsxtojson/comma.xlsx", sheet_name="pilkku")

recs = []

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
        "ID": row[0],"No_Controle" : row[1],"textQuestion": row[2],"_idTags": tagArray, "V-Values":v_values
        }

    print(rec)
    print()
    recs.append(rec)