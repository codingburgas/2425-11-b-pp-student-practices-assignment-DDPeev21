from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import PointInputForm
from app.extensions import db
import numpy as np
import matplotlib.pyplot as plt
import os
from uuid import uuid4

classifier_bp = Blueprint('classifier', __name__, template_folder='templates/classifier')

def perceptron_train(X, y, epochs=100):
    w = np.zeros(X.shape[1])
    for _ in range(epochs):
        for xi, yi in zip(X, y):
            if yi * (np.dot(w, xi)) <= 0:
                w += yi * xi
    return w

@classifier_bp.route('/classifier', methods=['GET', 'POST'])
def classify():
    form = PointInputForm()
    plot_url = None

    if form.validate_on_submit():
        try:
            raw = form.points.data.strip().splitlines()
            data = [list(map(float, line.split(','))) for line in raw]
            X = np.array([row[:2] for row in data])
            y = np.array([int(row[2]) for row in data])

            X_aug = np.hstack([X, np.ones((X.shape[0], 1))])  # add bias
            w = perceptron_train(X_aug, y)

            # Plotting
            fig, ax = plt.subplots()
            for point, label in zip(X, y):
                ax.plot(*point, 'ro' if label == 1 else 'bo')
            x_vals = np.linspace(X[:, 0].min(), X[:, 0].max(), 100)
            y_vals = -(w[0]*x_vals + w[2]) / w[1]
            ax.plot(x_vals, y_vals, 'k--')
            ax.set_title("Perceptron Classification")

            # Save plot
            filename = f"{uuid4().hex}.png"
            path = os.path.join("app", "static", "images", filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            fig.savefig(path)
            plot_url = url_for('static', filename=f'images/{filename}')

        except Exception as e:
            flash(f"Error processing input: {e}", 'danger')

    return render_template('classifier/classify.html', form=form, plot_url=plot_url)
