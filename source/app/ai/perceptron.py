# Perceptron logic will go here 

import numpy as np

class Perceptron:
    """A simple perceptron classifier for 2D points."""
    def __init__(self, input_size=2, lr=0.1, epochs=100):
        """
        Initialize the perceptron.
        :param input_size: Number of input features (default: 2)
        :param lr: Learning rate
        :param epochs: Number of training epochs
        """
        self.lr = lr
        self.epochs = epochs
        self.weights = np.zeros(input_size + 1)  # +1 for bias

    def predict(self, x):
        """
        Predict the class label for a single input.
        :param x: Input features (array-like)
        :return: Predicted class (0 or 1)
        """
        x = np.insert(x, 0, 1)  # Add bias term
        activation = np.dot(self.weights, x)
        return 1 if activation >= 0 else 0

    def fit(self, X, y):
        """
        Train the perceptron on the given data.
        :param X: Training data (2D array)
        :param y: Target labels (1D array)
        """
        X = np.c_[np.ones(X.shape[0]), X]  # Add bias column
        for _ in range(self.epochs):
            for xi, target in zip(X, y):
                update = self.lr * (target - self.predict(xi[1:]))
                self.weights += update * xi 