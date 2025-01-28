import os 
import sys

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityExcption

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifacts,
    DataValidationArtifacts,
    DataTransformationArtifacts, 
    ClassificationMetricArtifacts, 
    ModelTrainerArtifacts)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self)->DataIngestionArtifacts:
        try:
            logging.info("Initiating data ingestion...!!")
            dataingestionconfig = DataIngestionConfig(training_pipeline_config= self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config= dataingestionconfig)
            ingestion_artifacts = data_ingestion.initiate_data_ingestion()
            logging.info("data ingestion successfully initiated...!!")
            return ingestion_artifacts
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)

    def start_data_validation(self, ingestion_artifacts:DataIngestionArtifacts)->DataValidationArtifacts:
        try:
            logging.info("data validation has started..!!")
            datavalidationconfig = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact=ingestion_artifacts, data_validation_config=datavalidationconfig)
            logging.info("data validation is initiating...!!!")
            validation_artifacts = data_validation.initiate_data_validation()
            logging.info("data validation successfully completed...!!")
            return validation_artifacts
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        
    def start_data_transformation(self, validation_artifacts:DataValidationArtifacts)->DataTransformationArtifacts:
        try:
            logging.info("data Transformation has started..!!")
            datatransformationconfig = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifacts= validation_artifacts, data_transformation_config=datatransformationconfig)
            logging.info("data Transformation is initiating...!!!")
            transformation_artifacts = data_transformation.initiate_data_transformation()
            logging.info("data Transformation successfully completed...!!")
            return transformation_artifacts
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        
    def start_model_training(self, transformation_artifacts:DataTransformationArtifacts)->ModelTrainerArtifacts:
        try:
            logging.info("Model Training has started..!!")
            modeltrainerconfig = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(data_transformation_artifacts=transformation_artifacts, model_trainer_config=modeltrainerconfig)
            logging.info("Model Training is initiating...!!!")
            trainer_artifacts = model_trainer.initiate_model_trainer()
            logging.info("Model training is successfully completed...!!")
            return trainer_artifacts
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        
    def run_pipeline(self):
        try:
            # Data Ingestion...
            ingestion_artifacts = self.start_data_ingestion()

            #Data Validation...
            validation_artifacts = self.start_data_validation(ingestion_artifacts=ingestion_artifacts)

            # Data Transformation...
            transformation_artifacts = self.start_data_transformation(validation_artifacts=validation_artifacts)

            # Model trainer...
            model_trainer_artifacts = self.start_model_training(transformation_artifacts=transformation_artifacts)

            return model_trainer_artifacts

        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        