from networksecurity.entity.artifact_entity import DataIngestionArtifacts, DataValidationArtifacts #input will come from DataIngestionArtifacts and out put will store in DataValidationArtifacts..
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityExcption
from networksecurity.logging.logger import logging
from scipy.stats import ks_2samp #for checking data drift...
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
import pandas as pd
import os, sys


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifacts, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = pd.DataFrame(read_yaml_file(SCHEMA_FILE_PATH))
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        

    def validate_number_of_columns(self, dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self.schema_config) # we have made self.schema_config a data frame...
            logging.info(f"Required no of col: {number_of_columns}")
            logging.info(f"DataFrame has col: {len(dataframe.columns)}")
            if number_of_columns == len(dataframe.columns):
                return True
            return False
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        
    '''def validate_numerical_columns(self, dataframe:pd.DataFrame)->bool:
        try:
            df = self.schema_config
            status = []
            for col in df["numerical_columns"]:
                for dict in df["columns"]:
                    if col in dict:
                        for key,val in dict.items():
                            if val == 'int64':
                                status.append(True)
                            else:
                                status.append(False)  
                    else:
                        logging.info(f"Error: {col} is not in schema..!!")
                        status.append(False)

            logging.info(f"Status of num col: {status}")
            
            if False in status:
                return False
            return True
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)'''
    
    def detect_dataset_drift(self, base_df, current_df, threshold=0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2) # dist = distribution
                if threshold<=is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status": is_found
                    }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            #create directory 
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
            return status
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)


    def initiate_data_validation(self)->DataValidationArtifacts:
        try:
            train_file_path= self.data_ingestion_artifact.tarin_file_path
            test_file_path= self.data_ingestion_artifact.test_file_path
            # now read the data from this file path...
            train_df = self.read_data(train_file_path)
            test_df = self.read_data(test_file_path)
            # validation of number of col..
            train_data_validation = self.validate_number_of_columns(dataframe=train_df)
            if not train_data_validation:
                error_message = f"Train dataframe does not contains all columns.\n"

            test_data_validation = self.validate_number_of_columns(dataframe=test_df)
            if not test_data_validation:
                error_message = f"Test dataframe does not contains all columns.\n"

            '''# validation of numerical col..
            train_data_validation = self.validate_numerical_columns(dataframe=train_df)
            if not train_data_validation:
                error_message = f"Train dataframe has other than numerical columns.\n"

            test_data_validation = self.validate_numerical_columns(dataframe=test_df)
            if not test_data_validation:
                error_message = f"Test dataframe has other than numerical columns.\n"'''

            # Checking data drift...
            status = self.detect_dataset_drift(base_df=train_df, current_df= test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            #if status == True:
            train_df.to_csv(
                self.data_validation_config.valid_train_file_path, index = False, header=True
            )
            test_df.to_csv(
                self.data_validation_config.valid_test_file_path, index = False, header=True
            )

            data_validation_artifact = DataValidationArtifacts(
                validation_status = status,
                valid_train_file_path = self.data_ingestion_artifact.tarin_file_path,
                valid_test_file_path = self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path = None,
                drift_report_file_path = self.data_validation_config.drift_report_file_path 
            ) # here we store location of data_validtion output

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        
