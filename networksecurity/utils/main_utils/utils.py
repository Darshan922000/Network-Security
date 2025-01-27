# Here we write code for reading ymal file..
import yaml # from pyaml
from networksecurity.exception.exception import NetworkSecurityExcption
from networksecurity.logging.logger import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
import os, sys
import numpy as np
import dill
import pickle

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityExcption(e, sys)
    
def write_yaml_file(file_path: str, content: object, replace: bool = False)-> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityExcption(e, sys)
    
# for save numpy array and preprocessor object...
def save_numpy_array_data(file_path:str, array: np.array):
    """
    save numpy array data to file...
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityExcption(e, sys)

def save_oject(file_path:str, obj: object):
    try:
        logging.info("Enetred the save_object method of main unit class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj) # try to use dill here..!!
        logging.info("Exited the save_object method of main unit class")
    except Exception as e:
        raise NetworkSecurityExcption(e, sys)
    
def load_object(file_path: str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file {file_path} is not exists")

        logging.info("Enetred the load_object method of main unit class")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj) # try to use dill here..!!
        logging.info("Exited the load_object method of main unit class")

    except Exception as e:
        raise NetworkSecurityExcption(e, sys)
    

def load_numpy_array_data(file_path:str)->np.array:
    """
    load numpy array ...
    file_path: str location of file
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityExcption(e, sys)
    
def evaluate_models(X_train, y_train, X_test, y_test, models, params)->dict:
    try:
        report = {}

        for i in range(len(list(models))):

                model = list(models.values())[i]

                parameters = params[list(models.keys())[i]]

                gs = GridSearchCV(model, parameters, cv=3)
                gs.fit(X_train, y_train)

                model.set_params(**gs.best_params_)
                model.fit(X_train, y_train)

                logging.info(f"Hyperparameter is done...Best params = {model}")
                

                #model.fit(X_train, y_train)
                train_pred = model.predict(X_train)
                test_pred = model.predict(X_test)

                train_accuracy = r2_score(y_train, train_pred)
                test_accuracy = r2_score(y_test, test_pred)

                report[list(models.keys())[i]] = test_accuracy

        return report
    except Exception as e:
        raise NetworkSecurityExcption(e, sys)