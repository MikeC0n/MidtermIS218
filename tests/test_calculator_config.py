"""
Unit tests for the CalculatorConfig class.
"""

from decimal import Decimal
from pathlib import Path

import pytest

from app.exceptions import ConfigurationError
from app.calculator_config import CalculatorConfig, get_project_root


def test_default_values(monkeypatch):
    """Test that default values are set correctly when environment variables are not set."""
    # Unset environment variables
    monkeypatch.delenv('CALCULATOR_BASE_DIR', raising=False)
    monkeypatch.delenv('CALCULATOR_MAX_HISTORY_SIZE', raising=False)
    monkeypatch.delenv('CALCULATOR_AUTO_SAVE', raising=False)
    monkeypatch.delenv('CALCULATOR_PRECISION', raising=False)
    monkeypatch.delenv('CALCULATOR_MAX_INPUT_VALUE', raising=False)
    monkeypatch.delenv('CALCULATOR_DEFAULT_ENCODING', raising=False)
    monkeypatch.delenv('CALCULATOR_LOG_DIR', raising=False)
    monkeypatch.delenv('CALCULATOR_HISTORY_DIR', raising=False)
    monkeypatch.delenv('CALCULATOR_LOG_FILE', raising=False)
    monkeypatch.delenv('CALCULATOR_HISTORY_FILE', raising=False)

    config = CalculatorConfig()

    assert config.base_dir == get_project_root().resolve()
    assert config.max_history_size == 1000
    assert config.auto_save is True
    assert config.precision == 10
    assert config.max_input_value == Decimal('1e999')
    assert config.default_encoding == 'utf-8'
    assert config.log_dir == config.base_dir / "logs"
    assert config.history_dir == config.base_dir / "history"
    assert config.log_file == config.log_dir / "calculator.log"
    assert config.history_file == config.history_dir / "calculator_history.csv"


def test_environment_variable_overrides(monkeypatch):
    """Test that environment variables override default values."""
    monkeypatch.setenv('CALCULATOR_BASE_DIR', '/custom/base')
    monkeypatch.setenv('CALCULATOR_MAX_HISTORY_SIZE', '500')
    monkeypatch.setenv('CALCULATOR_AUTO_SAVE', 'false')
    monkeypatch.setenv('CALCULATOR_PRECISION', '5')
    monkeypatch.setenv('CALCULATOR_MAX_INPUT_VALUE', '1000')
    monkeypatch.setenv('CALCULATOR_DEFAULT_ENCODING', 'ascii')
    monkeypatch.setenv('CALCULATOR_LOG_DIR', '/custom/logs')
    monkeypatch.setenv('CALCULATOR_HISTORY_DIR', '/custom/history')
    monkeypatch.setenv('CALCULATOR_LOG_FILE', '/custom/logs/custom.log')
    monkeypatch.setenv('CALCULATOR_HISTORY_FILE', '/custom/history/custom_history.csv')

    config = CalculatorConfig()

    assert config.base_dir == Path('/custom/base').resolve()
    assert config.max_history_size == 500
    assert config.auto_save is False
    assert config.precision == 5
    assert config.max_input_value == Decimal('1000')
    assert config.default_encoding == 'ascii'
    assert config.log_dir == Path('/custom/logs').resolve()
    assert config.history_dir == Path('/custom/history').resolve()
    assert config.log_file == Path('/custom/logs/custom.log').resolve()
    assert config.history_file == Path('/custom/history/custom_history.csv').resolve()


def test_custom_initialization():
    """Test that custom initialization parameters are set correctly."""
    config = CalculatorConfig(
        base_dir=Path('/my/base'),
        max_history_size=200,
        auto_save=False,
        precision=15,
        max_input_value=Decimal('500'),
        default_encoding='iso-8859-1'
    )

    assert config.base_dir == Path('/my/base').resolve()
    assert config.max_history_size == 200
    assert config.auto_save is False
    assert config.precision == 15
    assert config.max_input_value == Decimal('500')
    assert config.default_encoding == 'iso-8859-1'


def test_validate_method():
    """Test that the validate method raises ConfigurationError for invalid values."""
    config = CalculatorConfig(
        max_history_size=-1,
        precision=0,
        max_input_value=Decimal('-100')
    )

    with pytest.raises(ConfigurationError, match="max_history_size must be positive"):
        config.validate()

    config.max_history_size = 1
    with pytest.raises(ConfigurationError, match="precision must be positive"):
        config.validate()

    config.precision = 1
    with pytest.raises(ConfigurationError, match="max_input_value must be positive"):
        config.validate()


def test_auto_save_parsing(monkeypatch):
    """Test that auto_save environment variable is parsed correctly."""
    test_cases = {
        '1': True,
        '0': False,
        'true': True,
        'false': False,
        'True': True,
        'False': False,
        'yes': False,
        'no': False,
        '': False,
        'random_string': False
    }

    for env_value, expected in test_cases.items():
        monkeypatch.setenv('CALCULATOR_AUTO_SAVE', env_value)
        config = CalculatorConfig()
        assert config.auto_save == expected


def test_log_dir_property(monkeypatch):
    """Test the log_dir property."""
    monkeypatch.setenv('CALCULATOR_LOG_DIR', '/custom/logs')
    config = CalculatorConfig()
    assert config.log_dir == Path('/custom/logs').resolve()


def test_history_dir_property(monkeypatch):
    """Test the history_dir property."""
    monkeypatch.setenv('CALCULATOR_HISTORY_DIR', '/custom/history')
    config = CalculatorConfig()
    assert config.history_dir == Path('/custom/history').resolve()


def test_log_file_property(monkeypatch):
    """Test the log_file property."""
    monkeypatch.setenv('CALCULATOR_LOG_FILE', '/custom/logs/custom.log')
    config = CalculatorConfig()
    assert config.log_file == Path('/custom/logs/custom.log').resolve()


def test_history_file_property(monkeypatch):
    """Test the history_file property."""
    monkeypatch.setenv('CALCULATOR_HISTORY_FILE', '/custom/history/custom_history.csv')
    config = CalculatorConfig()
    assert config.history_file == Path('/custom/history/custom_history.csv').resolve()
