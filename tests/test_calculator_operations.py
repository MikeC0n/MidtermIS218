"""
Unit tests for the calculatorOperations.py class.
"""

import datetime
from decimal import Decimal
import pytest

from app.exceptions import OperationError
from app.calculator_operations import CalculatorOperations


def test_addition():
    """Test addition operation."""
    calc = CalculatorOperations('Addition', Decimal('2'), Decimal('3'))
    assert calc.result == Decimal('5')


def test_subtraction():
    """Test subtraction operation."""
    calc = CalculatorOperations('Subtraction', Decimal('5'), Decimal('3'))
    assert calc.result == Decimal('2')


def test_multiplication():
    """Test multiplication operation."""
    calc = CalculatorOperations('Multiplication', Decimal('2'), Decimal('3'))
    assert calc.result == Decimal('6')


def test_division():
    """Test division operation."""
    calc = CalculatorOperations('Division', Decimal('6'), Decimal('3'))
    assert calc.result == Decimal('2')


def test_division_by_zero():
    """Test division by zero."""
    with pytest.raises(OperationError, match="Division by zero is not allowed"):
        CalculatorOperations('Division', Decimal('6'), Decimal('0'))


def test_power():
    """Test power operation."""
    calc = CalculatorOperations('Power', Decimal('2'), Decimal('3'))
    assert calc.result == Decimal('8')


def test_negative_exponent():
    """Test negative exponent."""
    with pytest.raises(OperationError, match="Negative exponents are not supported"):
        CalculatorOperations('Power', Decimal('2'), Decimal('-1'))


def test_root():
    """Test root operation."""
    calc = CalculatorOperations('Root', Decimal('16'), Decimal('2'))
    assert calc.result == Decimal('4')


def test_root_negative_operand():
    """Test root with negative operand."""
    with pytest.raises(OperationError, match="Cannot calculate root of negative number"):
        CalculatorOperations('Root', Decimal('-16'), Decimal('2'))


def test_root_zero_root():
    """Test root with zero as root."""
    with pytest.raises(OperationError, match="Zero root is undefined"):
        CalculatorOperations('Root', Decimal('16'), Decimal('0'))


def test_unknown_operation():
    """Test unknown operation."""
    with pytest.raises(OperationError, match="Unknown Operation: UnknownOp"):
        CalculatorOperations('UnknownOp', Decimal('2'), Decimal('3'))


def test_to_dict():
    """Test serialization to dictionary."""
    calc = CalculatorOperations('Addition', Decimal('2'), Decimal('3'))
    calc_dict = calc.to_dict()
    assert calc_dict['operation'] == 'Addition'
    assert calc_dict['operand1'] == '2'
    assert calc_dict['operand2'] == '3'
    assert calc_dict['result'] == '5'
    assert 'timestamp' in calc_dict


def test_from_dict():
    """Test deserialization from dictionary."""
    data = {
        'operation': 'Addition',
        'operand1': '2',
        'operand2': '3',
        'result': '5',
        'timestamp': datetime.datetime.now().isoformat()
    }
    calc = CalculatorOperations.from_dict(data)
    assert calc.operation == 'Addition'
    assert calc.operand1 == Decimal('2')
    assert calc.operand2 == Decimal('3')
    assert calc.result == Decimal('5')


def test_from_dict_invalid_data():
    """Test deserialization with invalid data."""
    data = {
        'operation': 'Addition',
        'operand1': '2',
        'operand2': '3',
        # 'result' key is missing
        'timestamp': datetime.datetime.now().isoformat()
    }
    with pytest.raises(OperationError, match="Invalid calculation data"):
        CalculatorOperations.from_dict(data)


def test_equality():
    """Test equality of two calculations."""
    calc1 = CalculatorOperations('Addition', Decimal('2'), Decimal('3'))
    calc2 = CalculatorOperations('Addition', Decimal('2'), Decimal('3'))
    assert calc1 == calc2


def test_inequality():
    """Test inequality of two calculations."""
    calc1 = CalculatorOperations('Addition', Decimal('2'), Decimal('3'))
    calc2 = CalculatorOperations('Addition', Decimal('2'), Decimal('4'))
    assert calc1 != calc2


def test_format_result():
    """Test formatting the result with precision."""
    calc = CalculatorOperations('Division', Decimal('1'), Decimal('3'))
    formatted_result = calc.format_result(precision=5)
    assert formatted_result == '0.33333'


def test_str_representation():
    """Test string representation."""
    calc = CalculatorOperations('Addition', Decimal('2'), Decimal('3'))
    assert str(calc) == 'Addition(2, 3) = 5'


def test_repr_representation():
    """Test repr representation."""
    calc = CalculatorOperations('Addition', Decimal('2'), Decimal('3'))
    expected_repr = (
        f"CalculatorOperations(operation='Addition', operand1=2, operand2=3, "
        f"result=5, timestamp={calc.timestamp.isoformat()})"
    )
    assert repr(calc) == expected_repr


def test_format_result_invalid_precision():
    """Test format_result with invalid precision."""
    calc = CalculatorOperations('Addition', Decimal('1'), Decimal('1'))
    formatted_result = calc.format_result(precision=-1)
    assert formatted_result == '2'
    