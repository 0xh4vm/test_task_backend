
class AuthResponse:
    BAD_FORMAT_PHONE_NUMBER = {"status": "Fail", "message": "Неверный формат номера телефона"}
    BAD_DATA_TYPE = {"status": "Fail", "message": "Неверный тип данных."}
    BAD_AUTH_DATA = {"status": "Fail", "message": "Неверный номер телефона или код авторизайции, попробуйте еще раз."}
    SUCCESS_AUTH_DATA = {"status": "OK"}
    UNKNOWNK_ERROR = {"status": "Fail", "message":"Неизвестная ошибка"}