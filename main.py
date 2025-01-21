from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityExcption
from networksecurity.logging.logger import logging
import sys

if __name__ == "__main__":
    try:
        logging.info("Initiating data ingestion...!!")
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(training_pipeline_config= trainingpipelineconfig)
        data_ingestion = DataIngestion(data_ingestion_config= dataingestionconfig)
        artifacts = data_ingestion.initiate_data_ingestion()
        logging.info("data ingestion successfully initiated...!!")
        print(artifacts)
    except Exception as e:
        raise NetworkSecurityExcption(e, sys)