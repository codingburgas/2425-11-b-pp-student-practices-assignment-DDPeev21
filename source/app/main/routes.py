import matplotlib
matplotlib.use('Agg')

# Main blueprint routes will go here 
from flask import render_template, send_file, make_response
from flask_login import login_required, current_user
from flask import Blueprint, redirect, url_for
from app.forms import PointForm, AdminUserEditForm
from app.ai.perceptron import Perceptron
from app.ai.logistic_regression import LogisticRegressionModel
from app.models import ClassifiedPoint, db, User
from flask import request, flash, abort
import numpy as np
import io
import matplotlib.pyplot as plt
import base64
import csv
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        plt.style.use('ggplot')
        # User chart
        user_points = ClassifiedPoint.query.filter_by(user_id=current_user.id).all()
        user_chart_image = None
        if user_points:
            xs = [p.x for p in user_points]
            ys = [p.y for p in user_points]
            results = [p.result for p in user_points]
            fig, ax = plt.subplots(figsize=(4,4))
            ax.scatter(xs, ys, c=results, cmap='coolwarm', s=80, edgecolor='black')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_title('Your Points')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            fig.subplots_adjust(left=0.18, right=0.98, top=0.88, bottom=0.18)
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
            buf.seek(0)
            user_chart_image = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close(fig)
        # Admin: all users chart
        is_admin = current_user.is_admin() if hasattr(current_user, 'is_admin') else False
        all_chart_image = None
        if is_admin:
            all_points = ClassifiedPoint.query.all()
            if all_points:
                xs = [p.x for p in all_points]
                ys = [p.y for p in all_points]
                results = [p.result for p in all_points]
                fig, ax = plt.subplots(figsize=(4,4))
                ax.scatter(xs, ys, c=results, cmap='coolwarm', s=80, edgecolor='black')
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_title('All Users Points')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                fig.subplots_adjust(left=0.18, right=0.98, top=0.88, bottom=0.18)
                buf = io.BytesIO()
                plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
                buf.seek(0)
                all_chart_image = base64.b64encode(buf.getvalue()).decode('utf-8')
                plt.close(fig)
        return render_template('main/index.html', user_chart_image=user_chart_image, all_chart_image=all_chart_image, is_admin=is_admin)
    return redirect(url_for('auth.login'))

@main.route('/classify', methods=['GET', 'POST'])
@login_required
def classify():
    form = PointForm()
    result = None
    img_data = None
    model_used = None
    warning = None
    if form.validate_on_submit():
        x = form.x.data
        y = form.y.data
        label = int(form.label.data)
        model_used = form.model.data
        # Add the new point with the true label
        point = ClassifiedPoint(user_id=current_user.id, x=x, y=y, label=label, result=-1)
        db.session.add(point)
        db.session.commit()

    # Fetch all classified points for the current user
    user_points = ClassifiedPoint.query.filter_by(user_id=current_user.id).all()
    if user_points:
        X_train = np.array([[p.x, p.y] for p in user_points])
        y_train = np.array([p.label for p in user_points])
        xs = [p.x for p in user_points]
        ys = [p.y for p in user_points]
        results = [p.result for p in user_points]
        plt.figure(figsize=(5,5))
        if form.model.data == 'logreg':
            unique_classes = np.unique(y_train)
            if len(unique_classes) < 2:
                warning = 'Logistic Regression requires at least 2 different classes in your data.'
            else:
                model = LogisticRegressionModel()
                model.fit(X_train, y_train, feature_names=['x', 'y'])
                if form.validate_on_submit():
                    result = int(model.predict(np.array([[x, y]]))[0])
                    point.result = result
                    db.session.commit()
                model_used = 'Logistic Regression'
                # Decision boundary for logistic regression
                x_min, x_max = X_train[:,0].min() - 0.5, X_train[:,0].max() + 0.5
                y_min, y_max = X_train[:,1].min() - 0.5, X_train[:,1].max() + 0.5
                xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200), np.linspace(y_min, y_max, 200))
                grid = np.c_[xx.ravel(), yy.ravel()]
                Z = model.predict(grid)
                Z = Z.reshape(xx.shape)
                plt.contourf(xx, yy, Z, alpha=0.2, cmap='coolwarm')
        else:
            perceptron = Perceptron()
            perceptron.fit(X_train, y_train)
            if form.validate_on_submit():
                result = perceptron.predict(np.array([x, y]))
                point.result = result
                db.session.commit()
            model_used = 'Perceptron'
            # Decision boundary for perceptron
            x_min, x_max = X_train[:,0].min() - 0.5, X_train[:,0].max() + 0.5
            y_min, y_max = X_train[:,1].min() - 0.5, X_train[:,1].max() + 0.5
            xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200), np.linspace(y_min, y_max, 200))
            grid = np.c_[xx.ravel(), yy.ravel()]
            Z = np.array([perceptron.predict(point) for point in grid])
            Z = Z.reshape(xx.shape)
            plt.contourf(xx, yy, Z, alpha=0.2, cmap='coolwarm')
        scatter = plt.scatter(xs, ys, c=results, cmap='coolwarm', s=120, edgecolor='black', label='Your Points')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(f'Your Classified Points ({model_used})')
        plt.legend()
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_data = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
    return render_template('main/classify.html', form=form, result=result, img_data=img_data, model_used=model_used, warning=warning)

@main.route('/history')
@login_required
def history():
    points = ClassifiedPoint.query.filter_by(user_id=current_user.id).order_by(ClassifiedPoint.timestamp.desc()).all()
    chart_image = None
    if points:
        plt.style.use('ggplot')
        xs = [p.x for p in points]
        ys = [p.y for p in points]
        results = [p.result for p in points]
        fig, ax = plt.subplots(figsize=(4,4))
        ax.scatter(xs, ys, c=results, cmap='coolwarm', s=80, edgecolor='black')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Your Classification Results Chart')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        fig.subplots_adjust(left=0.18, right=0.98, top=0.88, bottom=0.18)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)
        chart_image = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close(fig)
    return render_template('main/history.html', points=points, chart_image=chart_image)

@main.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        abort(403)
    plt.style.use('ggplot')
    users = User.query.all()
    points = ClassifiedPoint.query.order_by(ClassifiedPoint.timestamp.desc()).all()
    # Generate chart for all points
    chart_image = None
    if points:
        xs = [p.x for p in points]
        ys = [p.y for p in points]
        results = [p.result for p in points]
        fig, ax = plt.subplots(figsize=(4,4))
        ax.scatter(xs, ys, c=results, cmap='coolwarm', s=80, edgecolor='black')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('All Classified Points')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        fig.subplots_adjust(left=0.18, right=0.98, top=0.88, bottom=0.18)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)
        chart_image = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close(fig)
    return render_template('main/admin.html', users=users, points=points, chart_image=chart_image)

@main.route('/export-data')
@login_required
def export_data():
    # Get points for the current user
    points = ClassifiedPoint.query.filter_by(user_id=current_user.id).order_by(ClassifiedPoint.timestamp.desc()).all()
    
    # Create CSV in memory
    si = io.StringIO()
    cw = csv.writer(si)
    
    # Write header
    cw.writerow(['Timestamp', 'X', 'Y', 'Label', 'Result'])
    
    # Write data
    for point in points:
        cw.writerow([
            point.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            point.x,
            point.y,
            point.label,
            point.result
        ])
    
    # Create the response
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=user_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@main.route('/admin/export-data/<int:user_id>')
@login_required
def admin_export_data(user_id):
    if not current_user.is_admin():
        abort(403)
    
    # Get user data
    user = User.query.get_or_404(user_id)
    points = ClassifiedPoint.query.filter_by(user_id=user_id).order_by(ClassifiedPoint.timestamp.desc()).all()
    
    # Create CSV in memory
    si = io.StringIO()
    cw = csv.writer(si)
    
    # Write header
    cw.writerow(['Username', 'Timestamp', 'X', 'Y', 'Label', 'Result'])
    
    # Write data
    for point in points:
        cw.writerow([
            user.username,
            point.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            point.x,
            point.y,
            point.label,
            point.result
        ])
    
    # Create the response
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=user_{user.username}_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@main.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin():
        abort(403)
    user = User.query.get_or_404(user_id)
    form = AdminUserEditForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        user.confirmed = form.confirmed.data
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('main/edit_user.html', form=form, user=user)

@main.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin():
        abort(403)
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('main.admin_dashboard'))
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('main.admin_dashboard'))

@main.route('/logreg_results')
@login_required
def logreg_results():
    # Вземи всички точки на текущия потребител
    user_points = ClassifiedPoint.query.filter_by(user_id=current_user.id).all()
    metrics = None
    info_gain = None
    feature_names = ['x', 'y']
    img_data = None
    if user_points and len(user_points) > 2:
        X = np.array([[p.x, p.y] for p in user_points])
        y = np.array([p.label for p in user_points])
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LogisticRegressionModel()
        model.fit(X_train, y_train, feature_names=feature_names)
        average = 'binary' if len(np.unique(y)) == 2 else 'macro'
        metrics = model.evaluate(X_test, y_test, average=average)
        info_gain = model.get_information_gain()
        # --- Decision boundary visualization ---
        import matplotlib.pyplot as plt
        import io, base64
        plt.figure(figsize=(5,5))
        # Scatter user points
        scatter = plt.scatter(X[:,0], X[:,1], c=y, cmap='coolwarm', s=80, edgecolor='black', label='Points')
        # Mesh grid
        x_min, x_max = X[:,0].min() - 0.5, X[:,0].max() + 0.5
        y_min, y_max = X[:,1].min() - 0.5, X[:,1].max() + 0.5
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200), np.linspace(y_min, y_max, 200))
        grid = np.c_[xx.ravel(), yy.ravel()]
        Z = model.predict(grid)
        Z = Z.reshape(xx.shape)
        plt.contourf(xx, yy, Z, alpha=0.2, cmap='coolwarm')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Logistic Regression Decision Boundary')
        plt.legend()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_data = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
    return render_template('main/logreg_results.html', metrics=metrics, info_gain=info_gain, img_data=img_data) 