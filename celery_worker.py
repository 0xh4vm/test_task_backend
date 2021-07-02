from app import create_app, celery, make_celery


app = create_app()
make_celery(app)

from app.structure.routes import Structure