class CalculatorError(Exception):
    """Parent class for calculator exception handling."""
    pass

class ValidationError(CalculatorError): #Polymorphism/Inheritance
    """Raised when input validation fails."""
    pass

class OperationError(CalculatorError):
    """Raised when a calculation operation fails."""
    pass

class ConfigurationError(CalculatorError):
    """Raised when calculator configuration is invalid."""
    pass