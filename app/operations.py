from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict


class Operation(ABC):
    """Abstraction for calulator operations"""

    @abstractmethod
    def execute(self,a: Decimal, b: Decimal) -> Decimal: #Typing Hints
        """ 
        Execute Operation
        
        Arguments:
            a: first input
            b: second input

        Returns:
            Decimal: Result and format at the end of operation

        Raises:
            OperationEerror: If an operation fails and why for user readability
        """
        pass

    def validate_operands(sellf, a: Decimal, b: Decimal) -> None: # Example of data validation, sanitize inputs before execution
        """
        Data Validation before execution

        Arguments:
            a: First input
            b: Second input
        
        Raises:
            ValidationError: If input(s) are not valid numbers for calculation
        """
        pass

    def __str__(self) -> str:
        """Return operation name for display (ex. additon, subtraction, etc.)"""
        return self._class_._name_
    