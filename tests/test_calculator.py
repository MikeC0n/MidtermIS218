"""
Unit tests for the Calculator class.
"""

import datetime
from decimal import Decimal
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.calculator_operations import CalculatorOperations
from app.exceptions import OperationError, ValidationError
from app.history import HistoryObserver
from app.operations import Addition, OperationFactory

# Disable Pylint warnings about redefined outer name for the 'calculator' fixture
# pylint: disable=redefined-outer-name

@pytest.fixture
def calculator():
    """Fixture for Calculator instance with default config."""
    config = CalculatorConfig(
        base_dir=Path('/tmp/calculator_test'),
        max_history_size=100,
        auto_save=False
    )
    with patch('app.calculator.logging'), \
         patch.object(Calculator, 'load_history'), \
         patch.object(Calculator, 'save_history'):
        calc = Calculator(config)
    return calc


def test_calculator_initialization():
    """Test that the calculator initializes correctly."""
    with patch('app.calculator.logging'), \
         patch.object(Calculator, 'load_history'), \
         patch.object(Calculator, 'save_history'):
        calc = Calculator()
    assert calc.config is not None
    assert isinstance(calc.history, list)
    assert calc.operation_strategy is None
    assert isinstance(calc.observers, list)
    assert isinstance(calc.undo_stack, list)
    assert isinstance(calc.redo_stack, list)


def test_set_operation(calculator):
    """Test setting the operation strategy."""
    operation = Addition()
    calculator.set_operation(operation)
    assert calculator.operation_strategy == operation


def test_perform_operation(calculator):
    """Test performing an operation."""
    operation = Addition()
    calculator.set_operation(operation)
    result = calculator.perform_operation('2', '3')
    assert result == Decimal('5')
    assert len(calculator.history) == 1
    calc_op = calculator.history[-1]
    assert calc_op.operation == 'Addition'
    assert calc_op.operand1 == Decimal('2')
    assert calc_op.operand2 == Decimal('3')
    assert calc_op.result == Decimal('5')


def test_perform_operation_no_operation_set(calculator):
    """Test performing an operation without setting an operation strategy."""
    with pytest.raises(OperationError, match="No operation set"):
        calculator.perform_operation('2', '3')


def test_perform_operation_invalid_input(calculator):
    """Test performing an operation with invalid input."""
    operation = Addition()
    calculator.set_operation(operation)
    with pytest.raises(ValidationError, match="Invalid number format: invalid"):
        calculator.perform_operation('invalid', '3')


def test_add_observer(calculator):
    """Test adding an observer."""
    observer = Mock(spec=HistoryObserver)
    calculator.add_observer(observer)
    assert observer in calculator.observers


def test_remove_observer(calculator):
    """Test removing an observer."""
    observer = Mock(spec=HistoryObserver)
    calculator.add_observer(observer)
    calculator.remove_observer(observer)
    assert observer not in calculator.observers


def test_notify_observers(calculator):
    """Test notifying observers."""
    observer = Mock(spec=HistoryObserver)
    calculator.add_observer(observer)
    operation = Addition()
    calculator.set_operation(operation)
    calculator.perform_operation('2', '3')
    observer.update.assert_called_once()


def test_save_history(calculator):
    """Test saving history."""
    calculator.history.append(
        CalculatorOperations('Addition', Decimal('2'), Decimal('3'))
    )
    with patch('pandas.DataFrame.to_csv') as mock_to_csv:
        calculator.save_history()
        mock_to_csv.assert_called_once()


def test_load_history(calculator):
    """Test loading history."""
    data = pd.DataFrame([{
        'operation': 'Addition',
        'operand1': '2',
        'operand2': '3',
        'result': '5',
        'timestamp': datetime.datetime.now().isoformat()
    }])
    with patch('pandas.read_csv', return_value=data):
        calculator.load_history()
        assert len(calculator.history) == 1
        calc_op = calculator.history[0]
        assert calc_op.operation == 'Addition'
        assert calc_op.operand1 == Decimal('2')
        assert calc_op.operand2 == Decimal('3')
        assert calc_op.result == Decimal('5')


def test_clear_history(calculator):
    """Test clearing history."""
    calculator.history.append(
        CalculatorOperations('Addition', Decimal('2'), Decimal('3'))
    )
    calculator.clear_history()
    assert len(calculator.history) == 0
    assert len(calculator.undo_stack) == 0
    assert len(calculator.redo_stack) == 0


def test_undo_operation(calculator):
    """Test undoing an operation."""
    operation = Addition()
    calculator.set_operation(operation)
    calculator.perform_operation('2', '3')
    result = calculator.undo()
    assert result is True
    assert len(calculator.history) == 0
    assert len(calculator.undo_stack) == 0
    assert len(calculator.redo_stack) == 1


def test_undo_without_history(calculator):
    """Test undo when there's nothing to undo."""
    result = calculator.undo()
    assert result is False


def test_redo_operation(calculator):
    """Test redoing an operation."""
    operation = Addition()
    calculator.set_operation(operation)
    calculator.perform_operation('2', '3')
    calculator.undo()
    result = calculator.redo()
    assert result is True
    assert len(calculator.history) == 1
    assert len(calculator.undo_stack) == 1
    assert len(calculator.redo_stack) == 0


def test_redo_without_history(calculator):
    """Test redo when there's nothing to redo."""
    result = calculator.redo()
    assert result is False


def test_get_history_dataframe(calculator):
    """Test getting history as a DataFrame."""
    calculator.history = []  # Ensure history is empty
    calculator.history.append(
        CalculatorOperations('Addition', Decimal('2'), Decimal('3'))
    )
    df = calculator.get_history_dataframe()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]['operation'] == 'Addition'


def test_show_history(calculator):
    """Test showing history."""
    calculator.history = []  # Ensure history is empty
    calculator.history.append(
        CalculatorOperations('Addition', Decimal('2'), Decimal('3'), Decimal('5'))
    )
    history = calculator.show_history()
    assert len(history) == 1
    assert history[0] == 'Addition(2, 3) = 5'


def test_max_history_size(calculator):
    """Test that history does not exceed max history size."""
    calculator.config.max_history_size = 2
    calculator.history = []  # Ensure history is empty
    operation = Addition()
    calculator.set_operation(operation)
    calculator.perform_operation('1', '1')
    calculator.perform_operation('2', '2')
    calculator.perform_operation('3', '3')
    assert len(calculator.history) == 2
    assert calculator.history[0].operand1 == Decimal('2')
    assert calculator.history[1].operand1 == Decimal('3')


def test_operation_error_handling(calculator):
    """Test that operation errors are handled properly."""
    operation = OperationFactory.create_operation('divide')
    calculator.set_operation(operation)
    with pytest.raises(ValidationError, match="Division by zero is not allowed"):
        calculator.perform_operation('6', '0')
