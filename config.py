import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    SECRET_KEY = 'gwkghkf2934ysfljb45efsjfhkadslg2'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///' + os.path.join(basedir, "app.db")
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/test_task_backend'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

class TestConfig(object):
    DEBUG = True
    SECRET_KEY = 'gwkghkf2934ysfljb45efsjfhkadslg2'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///' + os.path.join(basedir, "test_app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
