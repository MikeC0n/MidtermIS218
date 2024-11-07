from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict
from app.exceptions import ValidationError


class Operation(ABC): # ABC class, sets up abstraction
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

    def validate_operands(sellf, a: Decimal, b: Decimal) -> None: # Example of data validation, sanitize inputs before completion
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

"""SOLID Principle, all classes perform one action"""
class Addition(Operation): # Polymorphism (Operation)
    """Addition Operation"""

    def execute(self, a: Decimal, b: Decimal) -> Decimal: # Inheritance, execute method from the operation class
        """Adding both inputs"""
        self.validate_operands(a, b) # Encapsulation, validation is immuatable and done through a method
        return a + b
    
class Subtraction(Operation):
    """Subtraction Operation"""

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Subtracting b from a"""
        self.validate_operands(a, b)
        return a - b

class Multiplication(Operation):
    """Multiplication Operation"""

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Multiplying both inputs together"""
        self.validate_operands(a, b)
        return a * b
    
class Division(Operation):
    """Division Operation"""

    def execute(self, a: Decimal, b: Decimal) -> None:
        """Validation of inputs, checking for divide by zero error"""
        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Division by zero is not allowed")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Division of a by b."""
        self.validate_operands(a, b)
        return a / b

class Power(Operation):
    """Exponential Function"""

    def validate_operands(sellf, a: Decimal, b: Decimal) -> None:
        """Validate input for accepted exponents"""
        super().validate_operands(a, b)
        if b < 0:
            raise ValidationError("Negative exponents are not allowed")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """Calculate a number, a, raised to the power b."""
        self.validate_operands(a, b)
        return Decimal(pow(float(a), float(b))) # Type casting

class Root(Operation):
    """Root Function"""

    def validate_operands(sellf, a: Decimal, b: Decimal) -> None:
        """Validate inputs for root operation"""
        super().validate_operands(a, b)
        if a < 0:
            raise ValidationError("Root of negative number cannot be calculated")
        if b == 0:
            raise ValidationError("Zero root is undefined")

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        self.validate_operands(a, b)
        return Decimal(pow(float(a), 1/float(b)))

# Factory Method
class OperationFactory:
    """Factory class for creating operation instances"""
    _operations: Dict[str, type] = { # Dictionary Implementation
        'add': Addition,
        'subtract': Subtraction,
        'multiply': Multiplication,
        'divide': Division,
        'power': Power,
        'root': Root
    }

    @classmethod
    def register_operation(cls, name: str, operation_class: type) -> None:
        """
        Cycle new operation type

        Arguments:
            name: Operation Name
            operation_class: Operation name pair in dictionary
        """
        if not issubclass(operation_class, Operation):
            raise TypeError("Operation class must inherit from Operation") # LBYL
        cls._operations[name.lower()] = operation_class

    @classmethod
    def create_operation(cls, operation_type: str) -> Operation:
        """
        Create operation instance

        Arguments:
            operation_type: type of operation to create

        Returns:
            Operation Instance

        Raises:
            ValueError: If the operation does not exist
        """
        operation_class = cls.operations.get(operation_type.lower())
        if not operation_class:
            raise ValueError(f"Unknown operation: {operation_type}")
        return operation_class()
