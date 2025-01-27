from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.exception.exception import NetworkSecurityExcption
from networksecurity.logging.logger import logging
import sys

if __name__ == "__main__":
    try:
        # Data Ingestion...
        logging.info("Initiating data ingestion...!!")
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(training_pipeline_config= trainingpipelineconfig)
        data_ingestion = DataIngestion(data_ingestion_config= dataingestionconfig)
        ingestion_artifacts = data_ingestion.initiate_data_ingestion()
        logging.info("data ingestion successfully initiated...!!")
        print(ingestion_artifacts)

        #Data Validation...
        logging.info("data validation has started..!!")
        datavalidationconfig = DataValidationConfig(training_pipeline_config=trainingpipelineconfig)
        data_validation = DataValidation(data_ingestion_artifact=ingestion_artifacts, data_validation_config=datavalidationconfig)
        logging.info("data validation is initiating...!!!")
        validation_artifacts = data_validation.initiate_data_validation()
        logging.info("data validation successfully completed...!!")
        print(validation_artifacts)

        # Data Transformation...
        logging.info("data Transformation has started..!!")
        datatransformationconfig = DataTransformationConfig(training_pipeline_config=trainingpipelineconfig)
        data_transformation = DataTransformation(data_validation_artifacts= validation_artifacts, data_transformation_config=datatransformationconfig)
        logging.info("data Transformation is initiating...!!!")
        transformation_artifacts = data_transformation.initiate_data_transformation()
        logging.info("data Transformation successfully completed...!!")
        print(transformation_artifacts)

        # Model trainer...
        logging.info("Model Training has started..!!")
        modeltrainerconfig = ModelTrainerConfig(training_pipeline_config=trainingpipelineconfig)
        model_trainer = ModelTrainer(data_transformation_artifacts=transformation_artifacts, model_trainer_config=modeltrainerconfig)
        logging.info("Model Training is initiating...!!!")
        trainer_artifacts = model_trainer.initiate_model_trainer()
        logging.info("Model training is successfully completed...!!")
        print(trainer_artifacts)
        


    except Exception as e:
        raise NetworkSecurityExcption(e, sys)