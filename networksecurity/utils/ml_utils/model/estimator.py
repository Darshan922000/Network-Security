from networksecurity.constant.training_pipeline import MODEL_FILE_NAME, SAVED_MODEL_DIR

import os
import sys

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityExcption

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model 
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        
    def predict(self, x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityExcption(e, sys)
        