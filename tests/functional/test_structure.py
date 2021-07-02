import json
from tests.functional.mocks.structure import *
from tests.functional.header import Header
from tests.functional.base import BaseTestCase
from app.structure.responses import StructureResponse
from pytest import raises
from requests.exceptions import ConnectionError, MissingSchema

class StructureTestCase(BaseTestCase):

    def wait_check_structure_result(self, task_id):
        with self.app.test_client() as test_client:
            response = test_client.get(f'/structure/check/{task_id}/')
            data = json.loads(response.data)

            while data == {'state': 'PENDING', 'status': 'Pending...'}:
                response = test_client.get(f'/structure/check/{task_id}/')
                data = json.loads(response.data)
            
            return data

    def test_structure_default_success(self):

        with self.app.test_client() as test_client:
            response = test_client.get('/structure/')
            assert response.status_code == 200
            assert json.loads(response.data) == DefaultMock.data

    def test_structure_status_code_onlinestringtools_success(self):

        with self.app.test_client() as test_client:
            response = test_client.get(f'/structure/?link={OnlinestringtoolsMock.url}')
            assert response.status_code == 200
            assert json.loads(response.data) == OnlinestringtoolsMock.data

    def test_structure_status_code_hackerone_success(self):

        with self.app.test_client() as test_client:
            response = test_client.get(f'/structure/?link={HackeroneMock.url}')
            assert response.status_code == 200
            assert json.loads(response.data) == HackeroneMock.data

    def test_structure_status_code_with_link_and_tags(self):

        with self.app.test_client() as test_client:
            response = test_client.get(f'/structure/?link={OnlinestringtoolsMock.url}&tags=div,p')
            assert response.status_code == 200
            assert json.loads(response.data) == {
                "div": 962, 
            }

    def test_check_structure_error_data_type(self):

        with self.app.test_client() as test_client:
            response = test_client.post('/structure/check/', data=json.dumps({}), headers=Header.json)
            assert response.status_code == 200
            assert json.loads(response.data) == StructureResponse.BAD_DATA_TYPE

    def test_check_structure_error_link_connection(self):

        with self.app.test_client() as test_client:
            with raises(ConnectionError):
                response = test_client.post('/structure/check/', data=json.dumps({"link": "http://asdasdasdasdasdafail.com", "structure": {}}), headers=Header.json)
                assert response.status_code == 200
                assert json.loads(response.data) == StructureResponse.BAD_REQUEST

    def test_check_structure_error_link_schema(self):

        with self.app.test_client() as test_client:
            with raises(MissingSchema):
                response = test_client.post('/structure/check/', data=json.dumps({"link": "fail", "structure": {}}), headers=Header.json)
                assert response.status_code == 200
                assert json.loads(response.data) == StructureResponse.BAD_REQUEST

    def test_check_structure_error_structure(self):
        
        with self.app.test_client() as test_client:
            response = test_client.post('/structure/check/', data=json.dumps({"link": OnlinestringtoolsMock.url, "structure": "fail"}))
            assert response.status_code == 200
            assert json.loads(response.data) == StructureResponse.BAD_DATA_TYPE

    def test_check_structure_is_correct(self):
        
        with self.app.test_client() as test_client:
            response = test_client.post('/structure/check/', data=json.dumps({
                "link": OnlinestringtoolsMock.url, 
                "structure": OnlinestringtoolsMock.data
            }), headers=Header.json)
            assert response.status_code == 200
            assert json.loads(response.data) == StructureResponse.SUCCESS_CHECK_STRUCTURE

    def test_check_structure_is_not_correct_left(self):

        fail_data = OnlinestringtoolsMock.data.copy()
        fail_data['div'] = 961

        with self.app.test_client() as test_client:
            response = test_client.post('/structure/check/', data=json.dumps({
                "link": OnlinestringtoolsMock.url, 
                "structure": fail_data
            }), headers=Header.json)
            data = json.loads(response.data)

            assert response.status_code == 200
            assert 'task_id' in data.keys()

            task_result = self.wait_check_structure_result(data.get('task_id'))
            assert task_result.get("is_correct") == False
            assert task_result.get("state") == 'SUCCESS'
            assert task_result.get("difference") == {"div": 1}

    def test_check_structure_is_not_correct_left_multiple(self):

        fail_data = HackeroneMock.data.copy()
        fail_data.update({
            "img": 30,
            "input": 1,
            "link": 1
        })

        with self.app.test_client() as test_client:
            response = test_client.post('/structure/check/', data=json.dumps({
                "link": HackeroneMock.url, 
                "structure": fail_data
            }), headers=Header.json)
            data = json.loads(response.data)

            assert response.status_code == 200
            assert 'task_id' in data.keys()

            task_result = self.wait_check_structure_result(data.get('task_id'))
            assert task_result.get("is_correct") == False
            assert task_result.get("state") == 'SUCCESS'
            assert task_result.get("difference") == {"img": 2, "input": 1, "link": 49}

    def test_check_structure_is_not_correct_right(self):

        fail_data = OnlinestringtoolsMock.data.copy()
        fail_data['h6'] = 7

        with self.app.test_client() as test_client:
            response = test_client.post('/structure/check/', data=json.dumps({
                "link": OnlinestringtoolsMock.url, 
                "structure": fail_data
            }), headers=Header.json)
            data = json.loads(response.data)

            assert response.status_code == 200
            assert 'task_id' in data.keys()

            task_result = self.wait_check_structure_result(data.get('task_id'))
            assert task_result.get("is_correct") == False
            assert task_result.get("state") == 'SUCCESS'
            assert task_result.get("difference") == {"h6": 7}

    def test_check_structure_is_not_correct_right_multiple(self):

        fail_data = HackeroneMock.data.copy()
        fail_data.update({
            "h6": 7,
            "asd": 1,
            "asdasd": 13234,
        })

        with self.app.test_client() as test_client:
            response = test_client.post('/structure/check/', data=json.dumps({
                "link": HackeroneMock.url, 
                "structure": fail_data
            }), headers=Header.json)
            data = json.loads(response.data)

            assert response.status_code == 200
            assert 'task_id' in data.keys()

            task_result = self.wait_check_structure_result(data.get('task_id'))
            assert task_result.get("is_correct") == False
            assert task_result.get("state") == 'SUCCESS'
            assert task_result.get("difference") == {"h6": 7, "asd": 1, "asdasd": 13234}

    def test_check_structure_is_not_correct_common(self):

        fail_data = HackeroneMock.data.copy()
        fail_data.update({
            "h6": 7,
            "asd": 1,
            "asdasd": 13234,
            "img": 30,
            "input": 1,
            "link": 1
        })

        with self.app.test_client() as test_client:
            response = test_client.post('/structure/check/', data=json.dumps({
                "link": HackeroneMock.url, 
                "structure": fail_data
            }), headers=Header.json)
            data = json.loads(response.data)

            assert response.status_code == 200
            assert 'task_id' in data.keys()

            task_result = self.wait_check_structure_result(data.get('task_id'))
            assert task_result.get("is_correct") == False
            assert task_result.get("state") == 'SUCCESS'
            assert task_result.get("difference") == {"h6": 7, "asd": 1, "asdasd": 13234, "img": 2, "input": 1, "link": 49}