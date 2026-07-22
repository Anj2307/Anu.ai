

from services.tools import calculator

import pytest

def test_add():
    assert calculator.invoke({
        "first_num": 5,
        "second_num": 3,
        "operation": "add"
    }) == 8


def test_subtract():
    assert calculator.invoke({
        "first_num": 8,
        "second_num": 5,
        "operation": "subtract"
    }) == 3


def test_multiply():
    assert calculator.invoke({
        "first_num": 4,
        "second_num": 6,
        "operation": "multiply"
    }) == 24


def test_divide():
    assert calculator.invoke({
        "first_num": 20,
        "second_num": 4,
        "operation": "divide"
    }) == 5

def test_divide_by_zero():

    with pytest.raises(ValueError):
        calculator.invoke({
            "first_num":10,
            "second_num":0,
            "operation":"divide"
        })