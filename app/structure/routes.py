from flask import request, jsonify, current_app
from flask.blueprints import DeferredSetupFunction
from flask_classy import FlaskView, route
from app.structure import DEFAULT_LINK, bp
import requests
import re
from app.structure.responses import StructureResponse
from app.decorators import check_get_request
from app.structure.celery_tasks import get_difference_structure
from celery.result import AsyncResult


class Structure(FlaskView):

    def set_args(self, link, tags=None):
        '''Установка параметров для обработки запросов'''
        self.link = link if link is not None else DEFAULT_LINK
        self.tags = tags.split(",") if tags is not None else None

        response = requests.get(self.link)

        self.source_code = response.text

    def get_structure(self):
        '''Получение структуры страницы'''
        pattern = "<([a-z]+[1-6]?)[\s>]" if self.tags is None else f"<({'|'.join(self.tags)})[\s>]"
        tags = re.findall(pattern, self.source_code, re.DOTALL | re.IGNORECASE)

        return {tag: tags.count(tag) for tag in set(tags)}

    def check_structure_correct(self, structure):
        '''Проверка структуры страницы'''
        right_structure = self.get_structure()

        if structure == right_structure:
            return StructureResponse.SUCCESS_CHECK_STRUCTURE
        
        task = get_difference_structure.delay(left_structure=structure, right_structure=right_structure)
        return {"task_id": task.id, "message": f"Для проверки статуса задачи перейдите /structure/check/{task.id}"}

    @check_get_request('link', DEFAULT_LINK, StructureResponse.BAD_REQUEST)
    def get(self):
        '''GET /structure/?link=<str:link>&tags=<str:tags>'''
        self.set_args(request.args.get("link"), request.args.get("tags"))
        structure = self.get_structure()

        return jsonify(structure), 200
    
    @route('/check/', methods=["POST"])
    def check_structure(self):
        '''POST /structure/check/ with data = {"link": <str:link>, "structure": <dict:structure>}'''
        if not request.is_json:
            return jsonify(StructureResponse.BAD_DATA_TYPE)

        link = request.json.get("link")
        structure = request.json.get("structure")

        if type(link) != str or type(structure) != dict:
            return jsonify(StructureResponse.BAD_DATA_TYPE)

        self.set_args(link)
        
        return jsonify(self.check_structure_correct(structure))

    @route('/check/<task_id>/', methods=["GET"])
    def check_task_status(self, task_id):
        '''GET /structure/check/<str:task_id>/'''
        task = get_difference_structure.AsyncResult(str(task_id))

        if task.state == 'PENDING': 
            return jsonify({'state': 'PENDING', 'status': 'Pending...'})
        
        elif task.state != 'FAILURE':
            return jsonify({"is_correct": False, 'state': task.state, "difference": task.info})
        
        else:
            return jsonify({'state': task.state, 'status': 'Fail'})

Structure.register(bp)
