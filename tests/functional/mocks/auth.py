from app import db
from app.models import AuthData

class AuthDataMock:
    phone_number = "+71231234567"
    code = "AAAAAA"

    @staticmethod
    def init():
        db.session.add(AuthData(phone_number=AuthDataMock.phone_number, code=AuthDataMock.code))
        db.session.commit()