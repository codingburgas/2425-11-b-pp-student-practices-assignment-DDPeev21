import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    precision_score, recall_score, f1_score, accuracy_score, confusion_matrix, log_loss
)
from sklearn.feature_selection import mutual_info_classif

class LogisticRegressionModel:
    def __init__(self, multi_class='auto', solver='lbfgs', max_iter=200):
        """
        multi_class: 'auto', 'ovr', or 'multinomial'
        solver: e.g. 'lbfgs', 'liblinear', etc.
        """
        self.model = LogisticRegression(multi_class=multi_class, solver=solver, max_iter=max_iter)
        self.is_fitted = False
        self.info_gain_ = None
        self.feature_names_ = None

    def fit(self, X, y, feature_names=None):
        self.model.fit(X, y)
        self.is_fitted = True
        if feature_names is not None:
            self.feature_names_ = feature_names
        # Information gain (mutual information)
        self.info_gain_ = mutual_info_classif(X, y)
        return self

    def predict(self, X):
        if not self.is_fitted:
            raise Exception("Model not fitted yet!")
        return self.model.predict(X)

    def predict_proba(self, X):
        if not self.is_fitted:
            raise Exception("Model not fitted yet!")
        return self.model.predict_proba(X)

    def evaluate(self, X, y_true, average='binary'):
        y_pred = self.predict(X)
        y_proba = self.predict_proba(X)
        # For binary, average='binary'; for multiclass, use 'macro' or 'weighted'
        metrics = {
            'precision': precision_score(y_true, y_pred, average=average, zero_division=0),
            'recall': recall_score(y_true, y_pred, average=average, zero_division=0),
            'f1_score': f1_score(y_true, y_pred, average=average, zero_division=0),
            'accuracy': accuracy_score(y_true, y_pred),
            'confusion_matrix': confusion_matrix(y_true, y_pred).tolist(),
            'logloss': log_loss(y_true, y_proba)
        }
        return metrics

    def get_information_gain(self):
        if self.info_gain_ is None:
            raise Exception("Model not fitted or info gain not calculated!")
        if self.feature_names_ is not None:
            return dict(zip(self.feature_names_, self.info_gain_))
        return self.info_gain_ 