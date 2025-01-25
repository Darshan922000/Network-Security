from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityExcption
from networksecurity.logging.logger import logging
import sys

if __name__ == "__main__":
    try:
        logging.info("Initiating data ingestion...!!")
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(training_pipeline_config= trainingpipelineconfig)
        data_ingestion = DataIngestion(data_ingestion_config= dataingestionconfig)
        ingestion_artifacts = data_ingestion.initiate_data_ingestion()
        logging.info("data ingestion successfully initiated...!!")
        print(ingestion_artifacts)
        logging.info("data validation has started..!!")
        datavalidationconfig = DataValidationConfig(training_pipeline_config=trainingpipelineconfig)
        data_validation = DataValidation(data_ingestion_artifact=ingestion_artifacts, data_validation_config=datavalidationconfig)
        logging.info("data validation is initiating...!!!")
        validation_artifacts = data_validation.initiate_data_validation()
        logging.info("data validation successfully completed...!!")
        print(validation_artifacts)
    except Exception as e:
        raise NetworkSecurityExcption(e, sys)