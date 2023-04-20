import requests
import pandas as pd
from dbutils import DBUtils
import csv

auth_params = {"email": "chandra.d@northeastern.edu", "password": "Diamond1220!"}
api_host = "https://www.disgenet.org/api"
api_key = "cf85fe28646e75646fc8969894d2fd55d06822af"

db = DBUtils('root', 'yourpasswd', 'gad', host='localhost')

m = []
with open("missing_diseases.csv", "r") as infile:
    for line in infile:
        d = line.strip()
        m.append(d)

diseases = pd.read_csv('diseases.csv')
diseaseId = set(diseases['diseaseId'].tolist())

for d in m:
    if d not in diseaseId:
        s = requests.Session()
        s.headers.update({"Authorization": "Bearer %s" % api_key})
    
        # getting disease attributes
        gda_response = s.get(api_host + '/disease/' + f'{d}')
        resp = gda_response.json()
        if "status_code" in resp:
            pass
        else:
            if s:
                s.close()
            for r in resp:
                # in format to insert to sql, no publication data in here
                r['num_pubs'] = 0
                dis = (r['diseaseid'], r['disease_name'], r['type'], r['disease_class'], r['disease_semantic_type'],
                       r['num_genes'], r['num_pubs'])
                try:
                    sql = "INSERT INTO diseases(diseaseId, diseaseName, diseaseType, diseaseClass, " \
                          "diseaseSemanticType, NofGenes, NofPmids) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    
                    db.insert_one(sql, dis)
                # when already in sql 
                except:
                    pass
                # insert into csv
                if r['diseaseid'] not in diseaseId:
                    row = list(dis)
                    with open('diseases.csv', 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(row)

