from dataclasses import dataclass


@dataclass
class DataIngestionArtifacts: #here we store location of data_ingestion output. 
    tarin_file_path: str 
    test_file_path: str 

@dataclass
class DataValidationArtifacts:  # here we store location of data_validtion output
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str

@dataclass
class DataTransformationArtifacts:  # here we store location of data_transformation output
    transformed_obj_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str

@dataclass
class ClassificationMetricArtifacts:
    f1_score: float
    precision_score: float
    recall_score: float

@dataclass
class ModelTrainerArtifacts:
    trained_model_file_path: str
    train_metric_artifacts: ClassificationMetricArtifacts
    test_metric_artifacts: ClassificationMetricArtifacts
