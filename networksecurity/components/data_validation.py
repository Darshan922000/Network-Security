from networksecurity.entity.artifact_entity import DataIngestionArtifacts, DataValidationArtifacts #input will come from DataIngestionArtifacts and out put will store in DataValidationArtifacts..
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityExcption
from networksecurity.logging.logger import logging
from scipy.stats import ks_2samp #for checking data drift...
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file
import pandas as pd
import os, sys


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifacts, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
