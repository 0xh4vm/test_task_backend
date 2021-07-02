from flask import json, request, jsonify
from flask_classy import FlaskView, route
import redis
from app import db, redis_client
from app.login.utils import randomword
from app.models import AuthData
from app.login import bp
import re
from app.login.responses import AuthResponse


class Login(FlaskView):

    def check_phone_number_format(self, phone_number):
        '''
        на клиентской стороне возможно стоит сделать навязывание кодов для выхода на международную связь
        здесь я предполагаю что интерфейс покажет клиенту формат в котором надо вводить телефон и ожидаю
        номер телефона в формате +[1-9][0-9]{10}, но для этого в ссылка должна иметь вид %2B[1-9][0-9]{10}
        '''
        return re.match("\+[1-9][0-9]{10}", phone_number)

    def check_phone_number_exists(self, phone_number):
        '''Попытка извлечь код из кеша или из бд, если нет в кеше. 
        Использую redis для того чтобы сократить количество обращений к бд'''
        code_from_cache = redis_client.get(phone_number)
    
        if code_from_cache is None:
            try:
                return AuthData.query.with_entities(AuthData.code).filter_by(phone_number=phone_number).first().code
            except:
                return None
        else:
            return code_from_cache

    def set_cache(self, phone_number, code):
        '''Инициаизация кеша'''
        if redis_client.get(phone_number) is None:
            redis_client.set(phone_number, code)

    def set_new_code(self, phone_number):
        '''Генерация нового кода доступа'''
        code = randomword()

        auth_data = AuthData(phone_number=phone_number, code=code)
        db.session.add(auth_data)
        db.session.commit()

        self.set_cache(phone_number=phone_number, code=code)

        return code

    def get(self):
        '''GET /login/?phone=<phone_number>'''
        try:
            phone_number = request.args.get("phone").strip()

            if not self.check_phone_number_format(phone_number):
                return jsonify(AuthResponse.BAD_FORMAT_PHONE_NUMBER)

            exist_code = self.check_phone_number_exists(phone_number)

            if exist_code is not None:
                self.set_cache(phone_number=phone_number, code=exist_code)
                return exist_code

            return self.set_new_code(phone_number)

        except:
            return jsonify(AuthResponse.UNKNOWNK_ERROR)

    def post(self):
        '''POST /login/ with data = {"phone": <str:phone_number>, "code": <str:code>}'''
        if not request.is_json:
            return jsonify(AuthResponse.BAD_DATA_TYPE)

        phone_number = request.json.get("phone")
        code = request.json.get("code")

        if AuthData.query.with_entities(AuthData.id).filter_by(phone_number=phone_number, code=code).first() is None:
            return jsonify(AuthResponse.BAD_AUTH_DATA)

        return jsonify(AuthResponse.SUCCESS_AUTH_DATA)

Login.register(bp)

