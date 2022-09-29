import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SOCKET_SECRET = os.environ.get('SECRET_KEY') or 'secret_key_guess_never'
    ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS') or ''
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False