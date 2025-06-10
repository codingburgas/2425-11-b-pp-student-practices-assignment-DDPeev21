import numpy as np
from utils.perceptron import Perceptron


def test_perceptron():
    X = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]])
    y = np.array([1, -1, -1, -1])  # AND-like labels

    model = Perceptron(epochs=100)
    model.fit(X, y)

    predictions = model.predict(X)
    assert np.array_equal(predictions, y)