import json
import pandas as pd

df = pd.read_excel("comma.xlsx", sheet_name="pilkku")

recs = []
#separate _idTags into individual words and create a array for them
#OR delete the idTags column from the comma.xlsx and from the list below (and fix the numbers)
#good to have: a smarter numbering system for the rows in the code

#"split tags at semicolon and check for duplicates and then create a list with ID:s"
for i, row in df.iterrows():
    rec = {
        "ID": row[0],"No_Controle" : row[1],"textQuestion": row[2],"_idTags": row[3],"V1": row[4],
        "V2": row[5],"V3": row[6],"V1A": row[7],"V4": row[8],"V4A": row[9],"V5": row[10],"V6": row[11],
        "V7": row[12],"V8": row[13],"V9": row[14],"V10": row[15],"V11": row[16],"V12": row[17],"V13": row[18],
        "V14": row[19],"V15": row[20],"V16": row[21],"V17": row[22],"V5A": row[23],"V18": row[24],"V19": row[25],
        "V20": row[26],"V": row[27],"V21": row[28],"V22": row[29],"V23": row[30],"V24": row[31],"V25": row[32],
        "V26": row[33],"V27": row[34],"V28": row[35],"V29": row[36],"V30": row[37],"V31": row[38],"VA21": row[39]
    }
    #"if the value is "non" in the V1-VA21, skip the value and don't include it in the rec
    #i = 4 if row[i] = "non" then pop it from the rec, i++
    recs.append(rec)

#save the response in a json file using pandas
print(recs)