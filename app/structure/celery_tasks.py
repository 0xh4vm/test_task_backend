from app import celery 

@celery.task
def get_difference_structure(left_structure, right_structure):
    difference = {tag: abs((right_structure[tag] if tag in right_structure else 0) - \
            (left_structure[tag] if tag in left_structure else 0)) \
            for tag in set(right_structure.keys()) | set(left_structure.keys())}

    return dict(filter(lambda x: x[1] != 0, difference.items()))