import sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityExcption

from networksecurity.entity.artifact_entity import ClassificationMetricArtifacts # Out put will store in that artifacts..
from sklearn.metrics import f1_score, precision_score, recall_score

def get_classification_score(y_true, y_pred)->ClassificationMetricArtifacts:
    try:
        f1 = f1_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        classification_metric = ClassificationMetricArtifacts(f1_score=f1, precision_score=precision, recall_score=recall)
        return classification_metric
    except Exception as e:
        raise NetworkSecurityExcption(e, sys)