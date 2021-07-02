from tests.functional.base import BaseTestCase
import json
from tests.functional.mocks.auth import AuthDataMock
from tests.functional.header import Header
from app.login.responses import AuthResponse


class AuthTestCase(BaseTestCase):
   
    def test_structure_auth_code_success_ru(self):
        with self.app.test_client() as test_client:
            response = test_client.get('/login/?phone=%2B79295649522')
            assert response.status_code == 201
            assert len(response.data) == 6

    def test_structure_auth_code_success_usa(self):
        with self.app.test_client() as test_client:
            response = test_client.get('/login/?phone=%2B19295649522')
            assert response.status_code == 201
            assert len(response.data) == 6

    def test_structure_auth_code_error_code_format_prefix(self):
        with self.app.test_client() as test_client:
            response = test_client.get('/login/?phone=+79295649522')
            assert response.status_code == 400
            assert json.loads(response.data) == AuthResponse.BAD_FORMAT_PHONE_NUMBER

    def test_structure_auth_code_error_code_format(self):

        with self.app.test_client() as test_client:
            response = test_client.get('/login/?phone=%2B09295649522')
            assert response.status_code == 400
            assert json.loads(response.data) == AuthResponse.BAD_FORMAT_PHONE_NUMBER

    def test_structure_auth_code_error_length(self):
        with self.app.test_client() as test_client:
            response = test_client.get('/login/?phone=%2B19295622')
            assert response.status_code == 400
            assert json.loads(response.data) == AuthResponse.BAD_FORMAT_PHONE_NUMBER

    def test_structure_auth_code_bad_key(self):
        with self.app.test_client() as test_client:
            response = test_client.get('/login/?phone_number=+19295622')
            assert response.status_code == 400
            assert json.loads(response.data) == AuthResponse.UNKNOWNK_ERROR
    def test_structure_check_code_success(self):
        with self.app.test_client() as test_client:
            
            AuthDataMock.init()

            response = test_client.post('/login/', data=json.dumps({
                "phone": AuthDataMock.phone_number,
                "code": AuthDataMock.code
            }), headers=Header.json)

            assert response.status_code == 200
            assert json.loads(response.data) == AuthResponse.SUCCESS_AUTH_DATA

    def test_structure_check_code_error_code(self):
        with self.app.test_client() as test_client:
            
            response = test_client.post('/login/', data=json.dumps({
                "phone": "+71231234567",
                "code": "AAAAAB"
            }), headers=Header.json)

            assert response.status_code == 400
            assert json.loads(response.data) == AuthResponse.BAD_AUTH_DATA
    
    def test_structure_check_code_error_phone(self):
        with self.app.test_client() as test_client:
            
            response = test_client.post('/login/', data=json.dumps({
                "phone": "+71231234568",
                "code": "AAAAAA"
            }), headers=Header.json)

            assert response.status_code == 400
            assert json.loads(response.data) == AuthResponse.BAD_AUTH_DATA
    
    def test_structure_check_code_error_without_code(self):
        with self.app.test_client() as test_client:
            
            response = test_client.post('/login/', data=json.dumps({
                "phone": "+71231234568",
            }), headers=Header.json)

            assert response.status_code == 400
            assert json.loads(response.data) == AuthResponse.BAD_AUTH_DATA

    def test_structure_check_code_error_without_phone(self):
        with self.app.test_client() as test_client:
            
            response = test_client.post('/login/', data=json.dumps({
                "code": "AAAAAA"
            }), headers=Header.json)

            assert response.status_code == 400
            assert json.loads(response.data) == AuthResponse.BAD_AUTH_DATA
