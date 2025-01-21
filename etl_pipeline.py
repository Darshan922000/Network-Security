import os 
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

import certifi
'''What certifi Does:
certifi is a Python package that provides a curated set of trusted Certificate Authority (CA) certificates.

Why certifi Is Needed:
It is used to verify the identity of secure (HTTPS) connections./
Libraries like requests or urllib3 use certifi to ensure they are connecting to trusted websites and not malicious ones.'''

ca = certifi.where() #it retrieve the part to the bundle of CA certificates provide by certifi and store in the variable ca.

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityExcption

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        
    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        
    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGODB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        
if __name__ == "__main__":
    FILE_PATH = "./Network_Data/phisingData.csv"
    DATABASE = "D9AI"
    COLLECTION = "MyNetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records = networkobj.insert_data_mongodb(records=records, database=DATABASE, collection=COLLECTION)
    print(no_of_records)


