import os


basedir = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(basedir, "..", ".."))

INSTANCE_DIR = os.path.join(ROOT_DIR, "instance")
if not os.path.exists(INSTANCE_DIR):
    os.makedirs(INSTANCE_DIR)


DATABASE_PATH = os.path.join(INSTANCE_DIR, 'placement.db')

class config:

    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'your_password_salt_here'

    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_TOKEN_AUTHENTICATION_METHODS = ['headers']
    SECURITY_REDIRECT_BEHAVIOR = 'spa'
    WTF_CSRF_ENABLED = False
    
    broker_url = 'redis://localhost:6379/0'
    result_backend = 'redis://localhost:6379/0'