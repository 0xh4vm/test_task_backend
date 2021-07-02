from app.login.utils import *
import re


def test_randomword_length_1():
    word = randomword(1)
    assert re.match("[A-Z0-9]{1}", word) is not None

def test_randomword_length_6():
    word = randomword(6)
    assert re.match("[A-Z0-9]{6}", word) is not None

def test_randomword_length_default():
    word = randomword()
    assert re.match("[A-Z0-9]{6}", word) is not None