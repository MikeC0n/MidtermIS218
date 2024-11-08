from abc import ABC, abstractmethod
import logging
from typing import Any
from app.calculatorOperations import calculatorOperations

class HistoryObserver(ABC):
    """Abstract class for calculator observers."""
    
    @abstractmethod
    def update(self, calculatorOperations: calculatorOperations) -> None:
        """
        Handle new calculator operation event.
        
        Args:
            calculatorOperations: The operation that was performed
        """
        pass

class LoggingObserver(HistoryObserver):
    """Observer that logs operations to file."""
    
    def update(self, calculatorOperations: calculatorOperations) -> None:
        """Log calculation details."""
        if calculatorOperations is None:
            raise AttributeError("Operation cannot be None")
        logging.info(
            f"Calculation performed: {calculatorOperations.operation} "
            f"({calculatorOperations.operand1}, {calculatorOperations.operand2}) = "
            f"{calculatorOperations.result}"
        )