from flask import Blueprint, render_template, request, flash, redirect, url_for  # Added Blueprint
from flask_login import login_required, current_user
from app import db
from app.models import DataPoint
from app.utils.perceptron import Perceptron
import numpy as np


# Fixed with Blueprint import and correct template folder
bp = Blueprint('main', __name__, template_folder='../../templates')

@bp.route('/')
@login_required
def home():
    return render_template('main/home.html')

@bp.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    if request.method == 'POST':
        try:
            x = float(request.form['x'])
            y = float(request.form['y'])
            label = int(request.form['label'])

            if label not in [0, 1]:
                flash('Label must be 0 or 1', 'danger')
                return redirect(url_for('main.survey'))

            point = DataPoint(x=x, y=y, label=label, user=current_user)
            db.session.add(point)
            db.session.commit()
            flash('Data point added successfully!', 'success')
            return redirect(url_for('main.survey'))
        except (ValueError, KeyError):
            flash('Invalid input. Please enter numeric values.', 'danger')

    return render_template('main/survey.html')

@bp.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    points = current_user.points.all()

    if len(points) < 2:
        flash('You need at least 2 data points to train the model', 'warning')
        return redirect(url_for('main.survey'))

    X = np.array([[p.x, p.y] for p in points])
    y = np.array([p.label for p in points])

    perceptron = Perceptron()
    perceptron.fit(X, y)

    result = None
    if request.method == 'POST':
        try:
            x = float(request.form['x'])
            y = float(request.form['y'])
            point_to_predict = np.array([[x, y]])
            result = perceptron.predict(point_to_predict)[0]
        except (ValueError, KeyError):
            flash('Invalid input. Please enter numeric values.', 'danger')

    return render_template('main/predict.html', result=result)