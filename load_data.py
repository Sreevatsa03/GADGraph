import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dbutils import DBUtils

# hardcoded to my acc info
auth_params = {"email": "chandra.d@northeastern.edu",
               "password": "Diamond1220!"}
api_host = "https://www.disgenet.org/api"
api_key = "cf85fe28646e75646fc8969894d2fd55d06822af"

db = DBUtils('root', 'yourpasswd', 'gad', host='localhost')


def clean_gene_tsv():
    """filters by # of publications, returns lst of genes + loads to sql"""
    gdf = pd.read_table('gene_associations.tsv')
    gdf = gdf[gdf['NofPmids'] >= 50]
    g_lst = []

    for row in gdf.itertuples(index=False):
        g_lst.append(tuple(row))

    sql = "INSERT INTO genes(geneId, geneSymbol, DSI, DPI, PLI, protein_class_name, protein_class, " \
          "NofDiseases, NofPmids) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    db.insert_many(sql, g_lst)
    print("GENES INSERT")
    g_id = gdf['geneId'].to_list()

    return g_id


def clean_disease_tsv():
    """insert available diseases into sql"""
    diseases_df = pd.read_table('disease_associations.tsv')
    diseases_df = diseases_df.fillna('NULL')

    d_lst = []
    for row in diseases_df.itertuples(index=False):
        d_lst.append(tuple(row))

    sql = "INSERT INTO diseases(diseaseId, diseaseName, diseaseType, diseaseClass, " \
          "diseaseSemanticType, NofGenes, NofPmids) VALUES(%s, %s, %s, %s, %s, %s, %s)"

    db.insert_many(sql, d_lst)
    print("dis insert")


def disgenAPI(batch):
    """calls gene > disease data from api per batch"""

    batch_lst = []
    for g in batch:
        s = requests.Session()
        # retries 3 times,
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        s.mount('http://', adapter)
        s.mount('https://', adapter)
        s.headers.update({"Authorization": "Bearer %s" % api_key})

        # gets responses of each gene in batch
        gda_response = s.get(api_host + '/gda/gene/' +
                             f'{g}', params={'min_ei': .75, 'min_score': .55})
        try:
            resp = gda_response.json()
        except ValueError:
            pass
        finally:
            if "status_code" in resp:
                pass
            else:
                s.close()
                for r in resp:
                    # in format to insert to sql
                    gad = (r['geneid'], r['diseaseid'], r['score'], r['ei'], r['el'], r['year_initial'],
                           r['year_final'], r['source'])
                    batch_lst.append(gad)

    return batch_lst


def call_api():
    """calls api, inserts in batches to sql"""
    genes = clean_gene_tsv()
    for i in range(0, len(genes), 25):
        batch = genes[i:(i + 25)]
        batch_lst = disgenAPI(batch)

        sql = "INSERT INTO gad(geneId, diseaseId, score, ei, el, yearInitial, yearFinal, g_source) " \
              "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        db.insert_many(sql, batch_lst)


def main():
    clean_disease_tsv()
    call_api()


if __name__ == "__main__":
    main()
