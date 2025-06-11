import numpy as np
import pickle

class Perceptron:
    def __init__(self, learning_rate=0.01, epochs=100):
        self.weights = None
        self.bias = None
        self.lr = learning_rate
        self.epochs = epochs

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.epochs):
            for idx, x_i in enumerate(X):
                linear_output = np.dot(x_i, self.weights) + self.bias
                y_pred = 1 if linear_output >= 0 else 0

                update = self.lr * (y[idx] - y_pred)
                self.weights += update * x_i
                self.bias += update

    def predict(self, X):
        linear_output = np.dot(X, self.weights) + self.bias
        return 1 if linear_output >= 0 else 0

def predict_point(point):
    with open("perceptron_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model.predict(np.array(point))
