"""
Unit tests for the custom exception classes in exceptions.py.
"""

import pytest

from app.exceptions import (
    CalculatorError,
    ValidationError,
    OperationError,
    ConfigurationError
)


def test_calculator_error():
    """Test that CalculatorError can be raised and caught."""
    with pytest.raises(CalculatorError) as exc_info:
        raise CalculatorError("Calculator error occurred")
    assert str(exc_info.value) == "Calculator error occurred"


def test_validation_error():
    """Test that ValidationError can be raised and caught."""
    with pytest.raises(ValidationError) as exc_info:
        raise ValidationError("Validation failed")
    assert str(exc_info.value) == "Validation failed"
    assert isinstance(exc_info.value, CalculatorError)


def test_operation_error():
    """Test that OperationError can be raised and caught."""
    with pytest.raises(OperationError) as exc_info:
        raise OperationError("Operation failed")
    assert str(exc_info.value) == "Operation failed"
    assert isinstance(exc_info.value, CalculatorError)


def test_configuration_error():
    """Test that ConfigurationError can be raised and caught."""
    with pytest.raises(ConfigurationError) as exc_info:
        raise ConfigurationError("Invalid configuration")
    assert str(exc_info.value) == "Invalid configuration"
    assert isinstance(exc_info.value, CalculatorError)


def test_inheritance():
    """Test the inheritance hierarchy of custom exceptions."""
    assert issubclass(ValidationError, CalculatorError)
    assert issubclass(OperationError, CalculatorError)
    assert issubclass(ConfigurationError, CalculatorError)
    assert issubclass(CalculatorError, Exception)
    