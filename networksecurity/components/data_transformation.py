import sys
import pandas as pd
import numpy as np

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityExcption

from networksecurity.entity.artifact_entity import DataValidationArtifacts, DataTransformationArtifacts #input will come from DataValidationArtifacts and out put will store in DataTransformationArtifacts..
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_oject


class DataTransformation:
    def __init__(self, data_validation_artifacts: DataValidationArtifacts, data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifacts = data_validation_artifacts
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)


    def get_data_transformer_object(cls)->Pipeline:
        """
        It initialises a KNNIputer object with the parameters specified in the training_pipeline.py file and 
        returns a Pipeline object with the KNNImputer object as the first step.

        Args:
            cls: DataTransformation

        Returns: 
            A pipeline object
        """
        logging.info("Entered get_data_transformer_object method of Transformation class")
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS) # Use ** to unpack the dictionary into KNNImputer
            logging.info("Initialized imputer...")
            processor: Pipeline = Pipeline([("imputer", imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)


    def initiate_data_transformation(self)->DataTransformationArtifacts:
        logging.info("Entered into method:initiate data transformation in class:DataTransformation")
        try:
           logging.info("Data Transformation has started")
           train_df = self.read_data(self.data_validation_artifacts.valid_train_file_path)
           test_df = self.read_data(self.data_validation_artifacts.valid_test_file_path)
           
           # Seperating Input Features and Target...
           X_train = train_df.drop(columns=TARGET_COLUMN, axis=1)
           y_train = train_df[TARGET_COLUMN]
           y_train = y_train.replace(-1, 0)

           X_test = test_df.drop(columns=TARGET_COLUMN, axis=1)
           y_test = test_df[TARGET_COLUMN]
           y_test = y_test.replace(-1, 0)

           preprocessor = self.get_data_transformer_object()
           preprocessor_obj = preprocessor.fit(X_train) #to save

           transformed_X_train = preprocessor_obj.transform(X_train)
           transformed_X_test = preprocessor_obj.transform(X_test)
           # Note: this two will give us an array...

           # let's combine Input featuers and Target via np.c_ (column wise)
           train_array = np.c_[transformed_X_train, np.array(y_train)] #to save
           test_array = np.c_[transformed_X_test, np.array(y_test)] # to save

           # lets save files..
           save_oject(file_path=self.data_transformation_config.data_transformed_obj_file_path, obj=preprocessor_obj)
           save_numpy_array_data(file_path=self.data_transformation_config.data_transformed_train_file_path, array=train_array)
           save_numpy_array_data(file_path=self.data_transformation_config.data_transformed_test_file_path, array=test_array)

           save_oject(file_path="final_model/preprocessor.pkl", obj=preprocessor_obj)

           #lets put the file locations in artifact_entity to use it for further process...
           data_transformation_artifacts = DataTransformationArtifacts(
               transformed_obj_file_path= self.data_transformation_config.data_transformed_obj_file_path, 
               transformed_train_file_path= self.data_transformation_config.data_transformed_train_file_path, 
               transformed_test_file_path= self.data_transformation_config.data_transformed_test_file_path
            )
           
           return data_transformation_artifacts


        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
