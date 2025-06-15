# Main blueprint routes will go here 
from flask import render_template, send_file
from flask_login import login_required, current_user
from flask import Blueprint, redirect, url_for
from app.forms import PointForm
from app.ai.perceptron import Perceptron
from app.models import ClassifiedPoint, db, User
from flask import request, flash, abort
import numpy as np
import io
import matplotlib.pyplot as plt
import base64

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('main/index.html')
    return redirect(url_for('auth.login'))

@main.route('/classify', methods=['GET', 'POST'])
@login_required
def classify():
    form = PointForm()
    result = None
    img_data = None
    if form.validate_on_submit():
        x = form.x.data
        y = form.y.data
        label = int(form.label.data)
        # Add the new point with the true label
        point = ClassifiedPoint(user_id=current_user.id, x=x, y=y, label=label, result=-1)
        db.session.add(point)
        db.session.commit()

    # Fetch all classified points for the current user
    user_points = ClassifiedPoint.query.filter_by(user_id=current_user.id).all()
    if user_points:
        X_train = np.array([[p.x, p.y] for p in user_points])
        y_train = np.array([p.label for p in user_points])
        perceptron = Perceptron()
        perceptron.fit(X_train, y_train)
        # Predict the class for the last input (if any)
        if form.validate_on_submit():
            result = perceptron.predict(np.array([x, y]))
            # Update the result for the last point
            point.result = result
            db.session.commit()
        xs = [p.x for p in user_points]
        ys = [p.y for p in user_points]
        results = [p.result for p in user_points]
        plt.figure(figsize=(5,5))
        scatter = plt.scatter(xs, ys, c=results, cmap='coolwarm', s=120, edgecolor='black', label='Your Points')
        x_vals = np.linspace(min(xs + [0])-0.2, max(xs + [1])+0.2, 100)
        plt.plot(x_vals, x_vals, 'k--', label='Decision Boundary (y=x)')
        plt.xlim(min(xs + [0])-0.2, max(xs + [1])+0.2)
        plt.ylim(min(ys + [0])-0.2, max(ys + [1])+0.2)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Your Classified Points')
        plt.legend()
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_data = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
    return render_template('main/classify.html', form=form, result=result, img_data=img_data)

@main.route('/history')
@login_required
def history():
    points = ClassifiedPoint.query.filter_by(user_id=current_user.id).order_by(ClassifiedPoint.timestamp.desc()).all()
    return render_template('main/history.html', points=points)

@main.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        abort(403)
    users = User.query.all()
    points = ClassifiedPoint.query.order_by(ClassifiedPoint.timestamp.desc()).all()
    return render_template('main/admin.html', users=users, points=points) 