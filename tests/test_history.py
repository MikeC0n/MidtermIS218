"""
Unit tests for the history observer classes.
"""

from unittest.mock import Mock, patch

import pytest

from app.calculator_operations import CalculatorOperations
from app.history import HistoryObserver, LoggingObserver, AutoSaveObserver


def test_history_observer_abstract():
    """Test that HistoryObserver cannot be instantiated and requires 'update' to be implemented."""
    with pytest.raises(TypeError):
        HistoryObserver() # pylint: disable=abstract-class-instantiated


def test_logging_observer_update_with_none():
    """Test that LoggingObserver raises AttributeError when calculator_operations is None."""
    observer = LoggingObserver()
    with pytest.raises(AttributeError, match="Operation cannot be None"):
        observer.update(None)


def test_logging_observer_update():
    """Test that LoggingObserver logs the correct message."""
    observer = LoggingObserver()
    calculator_operation = CalculatorOperations(
        operation='Addition',
        operand1=1,
        operand2=2
    )

    with patch('logging.info') as mock_logging_info:
        observer.update(calculator_operation)
        mock_logging_info.assert_called_once_with(
            f"Calculation performed: {calculator_operation.operation} "
            f"({calculator_operation.operand1}, {calculator_operation.operand2}) = "
            f"{calculator_operation.result}"
        )


def test_auto_save_observer_init_without_required_attributes():
    """Test that AutoSaveObserver raises TypeError when calculator lacks required attributes."""
    calculator_mock = Mock(spec=[])
    # Deliberately not setting 'config' and 'save_history'
    with pytest.raises(
        TypeError,
        match="Calculator must have 'config' and 'save_history' attributes"
    ):
        AutoSaveObserver(calculator_mock)


def test_auto_save_observer_update_with_none():
    """Test that AutoSaveObserver raises AttributeError when calculator_operations is None."""
    calculator_mock = Mock()
    calculator_mock.config = Mock(auto_save=True)
    calculator_mock.save_history = Mock()
    observer = AutoSaveObserver(calculator_mock)

    with pytest.raises(AttributeError, match="Operation cannot be None"):
        observer.update(None)


def test_auto_save_observer_update_auto_save_enabled():
    """Test that AutoSaveObserver calls save_history when auto_save is enabled."""
    calculator_mock = Mock()
    calculator_mock.config = Mock(auto_save=True)
    calculator_mock.save_history = Mock()

    observer = AutoSaveObserver(calculator_mock)
    calculator_operation = CalculatorOperations(
        operation='Addition',
        operand1=1,
        operand2=2
    )

    with patch('logging.info') as mock_logging_info:
        observer.update(calculator_operation)
        calculator_mock.save_history.assert_called_once()
        mock_logging_info.assert_called_once_with("History auto-saved")


def test_auto_save_observer_update_auto_save_disabled():
    """Test that AutoSaveObserver does not call save_history when auto_save is disabled."""
    calculator_mock = Mock()
    calculator_mock.config = Mock(auto_save=False)
    calculator_mock.save_history = Mock()

    observer = AutoSaveObserver(calculator_mock)
    calculator_operation = CalculatorOperations(
        operation='Addition',
        operand1=1,
        operand2=2
    )

    observer.update(calculator_operation)
    calculator_mock.save_history.assert_not_called()


def test_auto_save_observer_init_with_required_attributes():
    """Test that AutoSaveObserver initializes correctly with required attributes."""
    calculator_mock = Mock()
    calculator_mock.config = Mock()
    calculator_mock.save_history = Mock()

    observer = AutoSaveObserver(calculator_mock)
    assert observer.calculator == calculator_mock
