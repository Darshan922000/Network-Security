from networksecurity.exception.exception import NetworkSecurityExcption
from networksecurity.logging.logger import logging
import sys
import os
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifacts
from dotenv import load_dotenv
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URl")

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        
    def export_collection_as_dataframe(self):
        """
        Read the data from Mongodb
        """
        try:
            database_name =  self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGODB_URL)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop("_id", axis=1, inplace=True)

            df.replace({"na":np.nan}, inplace=True)
            return df
        
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # creating a folder...
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False, header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        
    def split_data(self, dataframe: pd.DataFrame):
        try:
            train_data, test_data = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split..!")

            train_data_path = self.data_ingestion_config.training_file_path
            test_data_path = self.data_ingestion_config.testing_file_path

            logging.info("Exporting train and test data into Ingested Folder..!")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            train_data = train_data.to_csv(train_data_path, index=False, header=True)
            test_data = test_data.to_csv(test_data_path, index=False, header=True)

            logging.info("Data Exported!")
            #return train_data, test_data
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data(dataframe)

            data_ingestion_artifacts = DataIngestionArtifacts(tarin_file_path= self.data_ingestion_config.training_file_path, test_file_path= self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifacts

        except Exception as e:
            raise NetworkSecurityExcption(e, sys)




