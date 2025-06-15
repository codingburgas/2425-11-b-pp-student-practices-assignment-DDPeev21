# Email sending logic will go here 

from flask_mail import Message
from flask import url_for, current_app
from itsdangerous import URLSafeTimedSerializer
from app import mail

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm-salt')

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt='email-confirm-salt',
            max_age=expiration
        )
    except Exception:
        return False
    return email

def send_confirmation_email(user):
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    subject = 'Please confirm your email'
    html = f'<p>Hi {user.username},</p>' \
           f'<p>Thanks for registering! Please confirm your email by clicking the link below:</p>' \
           f'<p><a href="{confirm_url}">{confirm_url}</a></p>'
    msg = Message(subject, recipients=[user.email], html=html)
    mail.send(msg) 