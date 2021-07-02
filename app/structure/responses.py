
class StructureResponse:
    BAD_DATA_TYPE = {"status": "Fail", "message": "Неверный тип данных."}
    SUCCESS_CHECK_STRUCTURE = {"is_correct": True}
    BAD_REQUEST = {"status": "Fail", "message": "Проблема получения страницы. Попробуйте позднее."}