from flask import Blueprint

bp = Blueprint('link', __name__)
DEFAULT_LINK = "https://freestylo.ru"

from app.structure import routes