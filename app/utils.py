from app import mail
from flask import url_for
from flask_mail import Message


def send_reset_email(reader):
    token = reader.get_reset_token()
    message = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[reader.email])
    message.body = f'''
    To reset your password, visit the following link:
    {url_for('readers.reset_token', token=token, _external=True)}
    
    if you did not make this request, ignore this email.
    '''

    mail.send(message)