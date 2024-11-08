from abc import ABC, abstractmethod
import logging
from typing import Any
from app.calculatorOperations import CalculatorOperations

class HistoryObserver(ABC):
    """Abstract class for calculator observers."""
    
    @abstractmethod
    def update(self, calculatorOperations: CalculatorOperations) -> None:
        """
        Handle new calculator operation event.
        
        Args:
            calculatorOperations: The operation that was performed
        """
        pass

class LoggingObserver(HistoryObserver):
    """Observer that logs operations to file."""
    
    def update(self, calculatorOperations: CalculatorOperations) -> None:
        """Log calculation details."""
        if calculatorOperations is None:
            raise AttributeError("Operation cannot be None")
        logging.info(
            f"Calculation performed: {calculatorOperations.operation} "
            f"({calculatorOperations.operand1}, {calculatorOperations.operand2}) = "
            f"{calculatorOperations.result}"
        )

class AutoSaveObserver(HistoryObserver):
    """Observer that automatically saves calculations."""
    
    def __init__(self, calculator: Any):
        if not hasattr(calculator, 'config') or not hasattr(calculator, 'save_history'):
            raise TypeError("Calculator must have 'config' and 'save_history' attributes")
        self.calculator = calculator

    def update(self, calculatorOperations: CalculatorOperations) -> None:
        """Trigger auto-save."""
        if calculatorOperations is None:
            raise AttributeError("Operation cannot be None")
        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("History auto-saved")