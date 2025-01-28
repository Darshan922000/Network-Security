import sys
import os
import pandas as pd
import numpy as np
import mlflow
import dagshub
dagshub.init(repo_owner='Darshan922000', repo_name='Network-Security', mlflow=True)

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityExcption

from networksecurity.entity.artifact_entity import DataTransformationArtifacts #input will come from here!!
from networksecurity.entity.artifact_entity import ClassificationMetricArtifacts, ModelTrainerArtifacts # Out put will store in that artifacts..

from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.utils.main_utils.utils import save_oject, load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data, evaluate_models

from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import (AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier)
from networksecurity.components.hyperparameter import parameter

class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifacts: DataTransformationArtifacts):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifacts = data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        
    def track_mlflow(self, best_model, classificationmetric):
        with mlflow.start_run():
            f1_score = classificationmetric.f1_score
            recall_score = classificationmetric.recall_score
            precision_score = classificationmetric.precision_score
            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("recall_score", recall_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.sklearn.log_model(best_model, "model")
        

    def train_model(self, X_train, y_train, X_test, y_test):
        models = {
            "Random Forest": RandomForestClassifier(verbose = 1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradiant Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "Adaboost": AdaBoostClassifier()
        }
        params = parameter

        model_report: dict = evaluate_models(X_train, y_train, X_test, y_test, models=models, params=params)

        best_model_score = max(model_report.values())
        best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
        best_model = models[best_model_name]

        y_train_pred = best_model.predict(X_train)
        y_test_pred = best_model.predict(X_test)

        train_classification_metrics = get_classification_score(y_pred=y_train_pred, y_true=y_train)
        # Tracking experiment with mlflow...
        self.track_mlflow(best_model=best_model, classificationmetric=train_classification_metrics)

        test_classification_metrics = get_classification_score(y_pred=y_test_pred, y_true=y_test)
        # Tracking test results with mlflow...
        self.track_mlflow(best_model=best_model, classificationmetric=test_classification_metrics)

        preprocessor = load_object(file_path=self.data_transformation_artifacts.transformed_obj_file_path)

        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)

        network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
        save_oject(file_path=self.model_trainer_config.trained_model_file_path, obj=network_model)

        logging.info("Best model is saved at ./file_model/")
        save_oject(file_path="final_model/model.pkl", obj=best_model)

        model_trainer_artifacts = ModelTrainerArtifacts(
            trained_model_file_path= self.model_trainer_config.trained_model_file_path, 
            train_metric_artifacts=train_classification_metrics, 
            test_metric_artifacts=test_classification_metrics
        )
        logging.info(f"Best Model: {best_model}")
        logging.info(f"Model Trainer Artifact: {model_trainer_artifacts}")
        return model_trainer_artifacts
    

    def initiate_model_trainer(self)->ModelTrainerArtifacts:
        try:
            train_file_path = self.data_transformation_artifacts.transformed_train_file_path
            test_file_path = self.data_transformation_artifacts.transformed_test_file_path

            #let's load data...
            train_array = load_numpy_array_data(train_file_path)
            test_array = load_numpy_array_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            model_trainer_artifacts = self.train_model(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)
            return model_trainer_artifacts

        except Exception as e:
            raise NetworkSecurityExcption(e, sys)