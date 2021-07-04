from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_redis import FlaskRedis
from celery import Celery


db = SQLAlchemy()
migrate = Migrate()
redis_client = FlaskRedis()
celery = Celery(__name__, backend=Config.CELERY_RESULT_BACKEND, broker=Config.CELERY_BROKER_URL)

def register_blueprints(app):
    from app.login import bp as login_bp
    app.register_blueprint(login_bp)

    from app.structure import bp as structure_bp
    app.register_blueprint(structure_bp)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    redis_client.init_app(app)

    register_blueprints(app)

    return app

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
