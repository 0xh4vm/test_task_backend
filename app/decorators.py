from functools import wraps
from flask import request, jsonify
import requests


def check_get_request(arg_name, default_link, error_message={"status": "Fail", "message": "Ошибка получения страницы"}):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                link = request.args.get(arg_name) if request.args.get(arg_name) is not None else default_link
                requests.get(link)
                return f(*args, **kwargs)
            except:
                return jsonify(error_message)

        return decorated_function
    return decorator
