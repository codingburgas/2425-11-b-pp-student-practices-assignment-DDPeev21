# Perceptron logic will go here 

import numpy as np

class Perceptron:
    def __init__(self, input_size=2, lr=0.1, epochs=100):
        self.lr = lr
        self.epochs = epochs
        self.weights = np.zeros(input_size + 1)  # +1 for bias

    def predict(self, x):
        x = np.insert(x, 0, 1)  # Add bias term
        activation = np.dot(self.weights, x)
        return 1 if activation >= 0 else 0

    def fit(self, X, y):
        X = np.c_[np.ones(X.shape[0]), X]  # Add bias column
        for _ in range(self.epochs):
            for xi, target in zip(X, y):
                update = self.lr * (target - self.predict(xi[1:]))
                self.weights += update * xi 