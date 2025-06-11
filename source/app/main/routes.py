from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import DataPoint
from ..utils.perceptron import Perceptron
from app.auth.forms import AddDataForm
from app.auth.forms import PointForm, AddDataForm
import numpy as np

bp = Blueprint('main', __name__, template_folder='../../templates')


X_train = np.array([[1, 1], [2, 2], [3, 3], [1, 0]])
y_train = np.array([1, 1, 1, 0])
model = Perceptron()
model.fit(X_train, y_train)

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
    form = PointForm()
    prediction = None

    points = current_user.points.all()
    if len(points) >= 2:
        X = np.array([[p.x, p.y] for p in points])
        y = np.array([p.label for p in points])
        model = Perceptron()
        model.fit(X, y)

        if form.validate_on_submit():
            x = form.x.data
            y = form.y.data
            prediction = model.predict(np.array([x, y]))
    else:
        flash('You need at least 2 data points to train the model', 'warning')
        return redirect(url_for('main.survey'))

    return render_template('main/predict.html', form=form, prediction=prediction)

@bp.route('/add-data', methods=['GET', 'POST'])
@login_required
def add_data():
    form = AddDataForm()
    if form.validate_on_submit():
        x = form.x.data
        y = form.y.data
        label = form.label.data
        point = DataPoint(x=x, y=y, label=label, user=current_user)
        db.session.add(point)
        db.session.commit()
        flash('Data point added!', 'success')
        return redirect(url_for('main.home'))
    return render_template('main/add_data.html', form=form)
