from dataclasses import dataclass, field
import datetime # Document accurate time
from decimal import Decimal, InvalidOperation
import logging # For logging purposes
from typing import Any, Dict

from app.exceptions import OperationError

@dataclass
class calculatorOperations:
    """Object representing a single operation."""
    
    # Required fields
    operation: str
    operand1: Decimal
    operand2: Decimal

    # End field with default value
    result: Decimal = field(init=False)
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    def __post_init__(self):
        """Calculation post initalization"""
        self.result = self.calculate()

    def calculate(self):
        """Main Calculation class, preforms appropriate operation based on dictionary vallidating inputs"""
        operations = {
            "Addition": lambda x, y: x + y,
            "Subtraction": lambda x, y: x - y,
            "Multiplication": lambda x, y: x * y,
            "Division": lambda x, y: x / y if y != 0 else self._raise_div_zero(),
            "Power": lambda x, y: Decimal(pow(float(x), float(y))) if y >= 0 else self._raise_neg_power(),
            "Root": lambda x, y: (
                Decimal(pow(float(x), 1/float(y))) 
                if x >= 0 and y != 0 
                else self._raise_invalid_root(x, y)
            )
        }

        OP = operations.get(self.operation)
        if not OP:
            raise OperationError(f"Unknown Operation: {self.operation}") # LBYL
        
        try:
            return OP(self.operand1, self.operand2)
        except (InvalidOperation, ValueError, ArithmeticError) as e:
            raise OperationError(f"Calculation failed: {str(e)}") # EAFP
        
    """Error Handling, LBYL"""
    @staticmethod
    def _raise_div_zero():
        """Helper method to raise divide by zero error."""
        raise OperationError("Division by zero is not allowed")

    @staticmethod
    def _raise_neg_power():
        """Helper method to raise negative power error."""
        raise OperationError("Negative exponents are not supported")

    @staticmethod
    def _raise_invalid_root(x: Decimal, y: Decimal):
        """Helper method to raise invalid root error."""
        if y == 0: # specifying errors and giving appropriate response
            raise OperationError("Zero root is undefined")
        if x < 0:
            raise OperationError("Cannot calculate root of negative number")
        raise OperationError("Invalid root operation")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert calculator operations to dict for serialization. For logging

        Returns:
            Dict containing the calculator operation data in serializable format
        """
        return {
            'opperation': self.operation,
            'operand1': str(self.operand1),
            'operand2': str(self.operand2),
            'result': str(self.result),
            'timestamp': self.timestamp.isoformat()
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'calculatorOperations':
        """
        Create calculation operation form dictionary for redo function.

        Arguments:
            data: Dictionary containing calculator operation data

        Returns:
            New calculatorOperations instance

        Raises:
            OperationError: If data is invalid or missing required fields
        """
        try:
            # Create the calculatorOperations object with the original operands
            calc = calculatorOperations(
                operation=data['operation'],
                operand1=Decimal(data['operand1']),
                operand2=Decimal(data['operand2'])
            )
        
            # set timestamp from saved data
            calc.timestamp = datetime.datetime.fromisoformat(data['timestamp'])

            # Data verification, checking for data mismatch
            saved_result = Decimal(data['result'])
            if calc.result != saved_result:
                logging.warning(
                    f"Loaded calculation result {saved_result} "
                    f"Different from computed result {calc.result}"
                )
        
            return calc
    
        except (KeyError, InvalidOperation, ValueError) as e:
            raise OperationError(f"Invalid calculation data: {str(e)}")

    def __str__(self) -> str:
        """
        Return string of calculation output.
        
        Returns:
            Formatted string showing the calculation and output.
        """
        return f"{self.operation}({self.operand1}, {self.operand2}) = {self.result}"
    
    def __repr__(self) -> str:
        """
        Return detailed string representation of calculator output.
        
        Returns:
            Detailed string showing all calculation attributes
        """
        return (
            f"Calculation(operation='{self.operation}', "
            f"operand1={self.operand1}, "
            f"operand2={self.operand2}, "
            f"result={self.result}, "
        )
    
    def __eq__(self, other: object) -> bool:
        """
        Check if two calculations are equal.

        Arguements:
            other; Another calculation to compare with

        Returns:
            True if calculations are equall, False otherwise
        """
        if not isinstance(other, calculatorOperations):
            return NotImplemented
        return (
            self.operation == other.operation and
            self.operand1 == other.operand1 and
            self.operand2 == other.operand2 and
            self.result == other.result
        )
    
    def format_result(self, precision: int = 10) -> str:
        """
        Format the output with specific precision.
        
        Args:
            precision: Number of decimal places to show
            
        Returns:
            Formatted string with number showing decimal places specified
        """
        try:
            # Remove trailing zeros and format to specified precision
            return str(self.result.normalize().quantize(
                Decimal('0.' + '0' * precision)
            ).normalize())
        except InvalidOperation: # EAFP
            return str(self.result)
