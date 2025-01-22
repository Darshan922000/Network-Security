import os
import sys
import numpy as np
import pandas as pd


"""
Defining common constant variable for training pipeline
"""
TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phisingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME: str = "MyNetworkData"
DATA_INGESTION_DATABASE_NAME: str = "D9AI"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2


"""
Data Validation related constant start with DATA_VALIDATION_VAR NAME
"""
DATA_VLIDATION_DIR_NAME: str = "data_validation"
DATA_VLIDATION_VALID_DIR: str = "validated"
DATA_VLIDATION_INVALID_DIR: str = "invalid"
DATA_VLIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VLIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"
