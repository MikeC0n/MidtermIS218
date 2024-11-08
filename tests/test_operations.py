"""
Unit tests for the operation classes and OperationFactory.
"""

from decimal import Decimal
import pytest

from app.exceptions import ValidationError
from app.operations import (
    Operation, Addition, Subtraction, Multiplication, Division, Power, Root, OperationFactory
)


def test_addition_execute():
    """Test the execute method of Addition."""
    addition = Addition()
    result = addition.execute(Decimal('2'), Decimal('3'))
    assert result == Decimal('5')


def test_subtraction_execute():
    """Test the execute method of Subtraction."""
    subtraction = Subtraction()
    result = subtraction.execute(Decimal('5'), Decimal('3'))
    assert result == Decimal('2')


def test_multiplication_execute():
    """Test the execute method of Multiplication."""
    multiplication = Multiplication()
    result = multiplication.execute(Decimal('2'), Decimal('3'))
    assert result == Decimal('6')


def test_division_execute():
    """Test the execute method of Division."""
    division = Division()
    result = division.execute(Decimal('6'), Decimal('3'))
    assert result == Decimal('2')


def test_division_by_zero():
    """Test Division by zero raises ValidationError."""
    division = Division()
    with pytest.raises(ValidationError, match="Division by zero is not allowed"):
        division.execute(Decimal('6'), Decimal('0'))


def test_power_execute():
    """Test the execute method of Power."""
    power = Power()
    result = power.execute(Decimal('2'), Decimal('3'))
    assert result == Decimal('8')


def test_power_negative_exponent():
    """Test Power with negative exponent raises ValidationError."""
    power = Power()
    with pytest.raises(ValidationError, match="Negative exponents are not allowed"):
        power.execute(Decimal('2'), Decimal('-1'))


def test_root_execute():
    """Test the execute method of Root."""
    root = Root()
    result = root.execute(Decimal('16'), Decimal('2'))
    assert result == Decimal('4')


def test_root_negative_number():
    """Test Root with negative number raises ValidationError."""
    root = Root()
    with pytest.raises(ValidationError, match="Root of negative number cannot be calculated"):
        root.execute(Decimal('-16'), Decimal('2'))


def test_root_zero_root():
    """Test Root with zero as root raises ValidationError."""
    root = Root()
    with pytest.raises(ValidationError, match="Zero root is undefined"):
        root.execute(Decimal('16'), Decimal('0'))


def test_operation_factory_create_known_operation():
    """Test that OperationFactory creates known operations correctly."""
    operation = OperationFactory.create_operation('add')
    assert isinstance(operation, Addition)

    operation = OperationFactory.create_operation('subtract')
    assert isinstance(operation, Subtraction)

    operation = OperationFactory.create_operation('multiply')
    assert isinstance(operation, Multiplication)

    operation = OperationFactory.create_operation('divide')
    assert isinstance(operation, Division)

    operation = OperationFactory.create_operation('power')
    assert isinstance(operation, Power)

    operation = OperationFactory.create_operation('root')
    assert isinstance(operation, Root)


def test_operation_factory_create_unknown_operation():
    """Test that OperationFactory raises ValueError for unknown operations."""
    with pytest.raises(ValueError, match="Unknown operation: unknown"):
        OperationFactory.create_operation('unknown')


def test_operation_factory_register_operation():
    """Test registering a new operation in OperationFactory."""

    class DummyOperation(Operation):
        """A dummy operation for testing purposes."""

        def execute(self, a: Decimal, b: Decimal) -> Decimal:
            return a

    OperationFactory.register_operation('dummy', DummyOperation)
    operation = OperationFactory.create_operation('dummy')
    assert isinstance(operation, DummyOperation)


def test_operation_factory_register_invalid_operation():
    """Test registering an invalid operation class raises TypeError."""

    class InvalidOperation: # pylint: disable=too-few-public-methods
        """An invalid operation class that does not inherit from Operation."""

    with pytest.raises(TypeError, match="Operation class must inherit from Operation"):
        OperationFactory.register_operation('invalid', InvalidOperation)


def test_operation_str():
    """Test the __str__ method of operations."""
    addition = Addition()
    assert str(addition) == 'Addition'

    subtraction = Subtraction()
    assert str(subtraction) == 'Subtraction'

    multiplication = Multiplication()
    assert str(multiplication) == 'Multiplication'

    division = Division()
    assert str(division) == 'Division'

    power = Power()
    assert str(power) == 'Power'

    root = Root()
    assert str(root) == 'Root'


def test_operation_validate_operands():
    """Test the default validate_operands method (should pass without error)."""
    addition = Addition()
    addition.validate_operands(Decimal('1'), Decimal('2'))  # Should not raise an exception
