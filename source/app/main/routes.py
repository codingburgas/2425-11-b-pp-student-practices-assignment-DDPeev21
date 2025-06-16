# Main blueprint routes will go here 
from flask import render_template, send_file
from flask_login import login_required, current_user
from flask import Blueprint, redirect, url_for
from app.forms import PointForm, AdminUserEditForm
from app.ai.perceptron import Perceptron
from app.models import ClassifiedPoint, db, User, Role
from flask import request, flash, abort
import numpy as np
import io
import matplotlib.pyplot as plt
import base64
from collections import Counter
from sqlalchemy import func

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        # Get points for the current user
        user_points = ClassifiedPoint.query.filter_by(user_id=current_user.id).all()
        
        # Prepare data for user's pie chart
        user_results = [point.result for point in user_points]
        user_result_counts = Counter(user_results)
        
        # Create user's pie chart with enhanced styling
        plt.figure(figsize=(8, 6))
        plt.pie(user_result_counts.values(), 
                labels=user_result_counts.keys(), 
                autopct='%1.1f%%',
                colors=['#2ecc71', '#27ae60', '#1abc9c', '#16a085'],  # Green palette
                shadow=True,
                startangle=90)
        plt.title('Your Classification Results', pad=20, fontsize=14, fontweight='bold')
        plt.axis('equal')
        
        # Save user's plot
        buf_user = io.BytesIO()
        plt.savefig(buf_user, format='png', bbox_inches='tight', dpi=300, facecolor='white')
        buf_user.seek(0)
        plt.close()
        
        # Convert to base64
        user_chart_image = base64.b64encode(buf_user.getvalue()).decode('utf-8')
        
        # If user is admin, also prepare overall statistics
        if current_user.is_admin():
            all_points = ClassifiedPoint.query.all()
            all_results = [point.result for point in all_points]
            all_result_counts = Counter(all_results)
            
            # Create overall pie chart with enhanced styling
            plt.figure(figsize=(8, 6))
            plt.pie(all_result_counts.values(), 
                    labels=all_result_counts.keys(), 
                    autopct='%1.1f%%',
                    colors=['#2ecc71', '#27ae60', '#1abc9c', '#16a085'],  # Green palette
                    shadow=True,
                    startangle=90)
            plt.title('Overall Classification Results', pad=20, fontsize=14, fontweight='bold')
            plt.axis('equal')
            
            # Save overall plot
            buf_all = io.BytesIO()
            plt.savefig(buf_all, format='png', bbox_inches='tight', dpi=300, facecolor='white')
            buf_all.seek(0)
            plt.close()
            
            # Convert to base64
            all_chart_image = base64.b64encode(buf_all.getvalue()).decode('utf-8')
            
            return render_template('main/index.html', 
                                user_chart_image=user_chart_image,
                                all_chart_image=all_chart_image,
                                is_admin=True)
        
        return render_template('main/index.html', 
                            user_chart_image=user_chart_image,
                            is_admin=False)
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
    
    # Prepare data for pie chart
    results = [point.result for point in points]
    result_counts = Counter(results)
    
    # Create pie chart
    plt.figure(figsize=(6, 4))
    plt.pie(result_counts.values(), labels=result_counts.keys(), autopct='%1.1f%%')
    plt.title('Your Classification Results')
    
    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    # Convert to base64 for embedding in HTML
    chart_image = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return render_template('main/history.html', points=points, chart_image=chart_image)

@main.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        abort(403)
    users = User.query.all()
    points = ClassifiedPoint.query.order_by(ClassifiedPoint.timestamp.desc()).all()
    
    # Prepare data for pie chart
    results = [point.result for point in points]
    result_counts = Counter(results)
    
    # Create pie chart
    plt.figure(figsize=(6, 4))
    plt.pie(result_counts.values(), labels=result_counts.keys(), autopct='%1.1f%%')
    plt.title('Overall Classification Results')
    
    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    # Convert to base64 for embedding in HTML
    chart_image = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return render_template('main/admin.html', users=users, points=points, chart_image=chart_image)

@main.route('/admin/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin():
        abort(403)
    user = User.query.get_or_404(user_id)
    form = AdminUserEditForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.confirmed = form.confirmed.data
        role = Role.query.filter_by(name=form.role.data).first()
        if role:
            user.role = role
        db.session.commit()
        flash('User updated successfully!')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('main/edit_user.html', form=form, user=user)

@main.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin():
        abort(403)
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete your own account!', 'danger')
        return redirect(url_for('main.admin_dashboard'))
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!')
    return redirect(url_for('main.admin_dashboard')) 