"""Tests for the calculator command."""

import pytest
from assistant.commands.calculator import handle_calculator, _safe_eval


class TestSafeEval:
    def test_addition(self):
        assert _safe_eval("2 + 3") == 5

    def test_subtraction(self):
        assert _safe_eval("10 - 4") == 6

    def test_multiplication(self):
        assert _safe_eval("3 * 7") == 21

    def test_division(self):
        assert _safe_eval("10 / 4") == 2.5

    def test_power(self):
        assert _safe_eval("2 ** 10") == 1024

    def test_power_caret(self):
        assert _safe_eval("2^8") == 256

    def test_modulo(self):
        assert _safe_eval("10 % 3") == 1

    def test_negative_unary(self):
        assert _safe_eval("-5") == -5

    def test_parentheses(self):
        assert _safe_eval("(2 + 3) * 4") == 20

    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            _safe_eval("5 / 0")

    def test_invalid_expression(self):
        with pytest.raises(ValueError):
            _safe_eval("import os")


class TestHandleCalculator:
    def test_basic_addition(self):
        response = handle_calculator("calculate 1 + 1")
        assert "2" in response

    def test_natural_language(self):
        response = handle_calculator("what is 10 * 5")
        assert "50" in response

    def test_result_contains_expression(self):
        response = handle_calculator("2 + 2")
        assert "4" in response

    def test_division_by_zero_message(self):
        response = handle_calculator("10 / 0")
        assert "zero" in response.lower()

    def test_integer_result_formatting(self):
        response = handle_calculator("6 / 2")
        assert "3" in response
        assert "3.0" not in response

    def test_empty_query(self):
        response = handle_calculator("")
        assert "expression" in response.lower()

    def test_complex_expression(self):
        response = handle_calculator("(2 + 3) * 4")
        assert "20" in response
