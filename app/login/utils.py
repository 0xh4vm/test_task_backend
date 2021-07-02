from random import choice
import string

def randomword(length=6) -> str:
    '''Функция генерации кода'''
    letters = string.ascii_uppercase + string.digits
    return ''.join(choice(letters) for i in range(length))