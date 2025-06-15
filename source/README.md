# Simple Linearly Separable Classifier

A modern Flask web app for classifying 2D points using a perceptron. Includes user authentication, email confirmation, profile management, admin dashboard, and interactive AI visualization.

## Features
- User registration, login, logout (with email confirmation)
- User roles: regular user and admin
- Profile management (edit username/email)
- Classify 2D points using a perceptron
- View classification history and results
- Visualize classified points on a 2D plot
- Admin dashboard to view all users and classifications
- Custom error pages (404, 500)
- Responsive, beautiful Bootstrap interface

## Setup Instructions
1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set environment variables** (for email sending):
   - `SECRET_KEY` (for Flask security)
   - `MAIL_USERNAME` (your email address)
   - `MAIL_PASSWORD` (your email password or app password)
4. **Initialize the database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```
5. **Run the app**
   ```bash
   flask run
   ```

## Usage
- Register a new account and confirm your email.
- Log in to access the dashboard.
- Classify points and view your history and visualizations.
- Admins can access the admin dashboard to manage users and view all data.

## Project Structure
```
app/
  ai/              # Perceptron logic
  auth/            # Authentication blueprint
  errors/          # Error handlers
  main/            # Main app logic
  user/            # User profile blueprint
  static/          # Static files
  templates/       # Jinja2 templates
  email.py         # Email logic
  forms.py         # WTForms
  models.py        # SQLAlchemy models
  __init__.py      # App factory
config.py          # Configuration
run.py             # Entry point
requirements.txt   # Dependencies
README.md          # This file
```

## Notes
- For email confirmation, use a Gmail account or configure your own SMTP server.
- To create an admin, manually set a user's role to 'admin' in the database.
- The perceptron is trained on simple demo data; you can extend it for more advanced use.

---
**Enjoy your modern Flask AI app!** 