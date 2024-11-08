"""
Unit tests for the InputValidator class.
"""

from decimal import Decimal
import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.input_validators import InputValidator


def test_validate_number_with_valid_int():
    """Test validate_number with a valid integer."""
    config = CalculatorConfig(max_input_value=Decimal('1000'))
    result = InputValidator.validate_number(123, config)
    assert result == Decimal('123')


def test_validate_number_with_valid_float():
    """Test validate_number with a valid float."""
    config = CalculatorConfig(max_input_value=Decimal('1000'))
    result = InputValidator.validate_number(123.456, config)
    assert result == Decimal('123.456')


def test_validate_number_with_valid_str():
    """Test validate_number with a valid string number."""
    config = CalculatorConfig(max_input_value=Decimal('1000'))
    result = InputValidator.validate_number('789', config)
    assert result == Decimal('789')


def test_validate_number_with_valid_str_float():
    """Test validate_number with a valid string float."""
    config = CalculatorConfig(max_input_value=Decimal('1000'))
    result = InputValidator.validate_number('789.012', config)
    assert result == Decimal('789.012')


def test_validate_number_with_whitespace_str():
    """Test validate_number with a string containing whitespace."""
    config = CalculatorConfig(max_input_value=Decimal('1000'))
    result = InputValidator.validate_number('  345.678  ', config)
    assert result == Decimal('345.678')


def test_validate_number_exceeds_max_value():
    """Test validate_number with a number exceeding max_input_value."""
    config = CalculatorConfig(max_input_value=Decimal('1000'))
    with pytest.raises(ValidationError, match="Value exceeds maximum allowed: 1000"):
        InputValidator.validate_number('1001', config)


def test_validate_number_with_invalid_str():
    """Test validate_number with an invalid string."""
    config = CalculatorConfig(max_input_value=Decimal('1000'))
    with pytest.raises(ValidationError, match="Invalid number format: invalid"):
        InputValidator.validate_number('invalid', config)


def test_validate_number_with_none():
    """Test validate_number with None."""
    config = CalculatorConfig(max_input_value=Decimal('1000'))
    with pytest.raises(ValidationError, match="Invalid number format: None"):
        InputValidator.validate_number(None, config)


def test_validate_number_with_complex_type():
    """Test validate_number with an unsupported type (tuple)."""
    config = CalculatorConfig(max_input_value=Decimal('1000'))
    with pytest.raises(ValidationError, match=r"Invalid number format: \('1', '2'\)"):
        InputValidator.validate_number(('1', '2'), config)


def test_validate_number_with_negative_number():
    """Test validate_number with a negative number."""
    config = CalculatorConfig(max_input_value=Decimal('1000'))
    result = InputValidator.validate_number('-500', config)
    assert result == Decimal('-500')


def test_validate_number_negative_exceeds_max_value():
    """Test validate_number with a negative number exceeding max_input_value."""
    config = CalculatorConfig(max_input_value=Decimal('1000'))
    with pytest.raises(ValidationError, match="Value exceeds maximum allowed: 1000"):
        InputValidator.validate_number('-1001', config)


def test_validate_number_with_zero():
    """Test validate_number with zero."""
    config = CalculatorConfig(max_input_value=Decimal('1000'))
    result = InputValidator.validate_number('0', config)
    assert result == Decimal('0')


def test_validate_number_with_large_number_within_limit():
    """Test validate_number with a large number within max_input_value."""
    config = CalculatorConfig(max_input_value=Decimal('1e10'))
    result = InputValidator.validate_number('9999999999', config)
    assert result == Decimal('9999999999')


def test_validate_number_with_special_characters():
    """Test validate_number with a string containing special characters."""
    config = CalculatorConfig(max_input_value=Decimal('1000'))
    with pytest.raises(ValidationError, match=r"Invalid number format: \$123"):
        InputValidator.validate_number('$123', config)


def test_validate_number_with_scientific_notation():
    """Test validate_number with scientific notation."""
    config = CalculatorConfig(max_input_value=Decimal('1e10'))
    result = InputValidator.validate_number('1e3', config)
    assert result == Decimal('1000')


def test_validate_number_with_infinite():
    """Test validate_number with infinity."""
    config = CalculatorConfig(max_input_value=Decimal('1000'))
    with pytest.raises(ValidationError, match="Value exceeds maximum allowed: 1000"):
        InputValidator.validate_number('Infinity', config)
