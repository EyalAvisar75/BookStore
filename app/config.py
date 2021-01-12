import os


class Config:
    SECRET_KEY = '46f515d48430c7694202e92b0b466f21'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
