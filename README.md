# Midterm IS218 Calculator
This is a Python repository for a calculator program that demonstrates principles of programming including but not limited to Object-Oriented Programming, Factory Method, REPL, EAFP, Environment Variables, and Logging. 
## [Demonstration Video](https://youtu.be/5A_keBOVjJM)

# Install

1. Clone Repository:
```bash
   git clone https://github.com/yourusername/MidtermIS218.git
   cd MidtermIS218.git
```
2. Set up the virtual environment and install dependencies:
```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
```

3. To set up the environment variables, create a `.env` file in the project root:
```env
   CALCULATOR_BASE_DIR=/path/to/base/dir
   CALCULATOR_MAX_HISTORY_SIZE=100
   CALCULATOR_AUTO_SAVE=true
   CALCULATOR_PRECISION=10
   CALCULATOR_MAX_INPUT_VALUE=1e100
   CALCULATOR_DEFAULT_ENCODING=utf-8
```
4. Run the program:
 ```bash
   python3 main.py
 ```


# Calculator Features
  - **Arithmetic Functions**
      - add, subtract, multiply, divide, power, root
  - **Calculator History Functions**
      - history: Shows all past calculations currently saved in the instance
      - clear: Clears all history loaded on the current calculator instance
      - undo/redo: Remove last operation/Retrieve last deleted operation
  - **History CSV Functions**
      - save/load: Save current history to CSV/Load saved history CSV

- ## Principles
   - Object-Oriented Programming (From calculator.py (Line 11 - 16))
```python
from app.calculator_operations import CalculatorOperations
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, HistoryObserver, LoggingObserver
from app.input_validators import InputValidator
from app.operations import Operation, OperationFactory
...
```
   - Factory Method (From operations.py (Line 113 - 122))
```python
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
...
```
   - REPL (From calculator.py (Line 242 - 254, Line 271 - 287))
```python
def calculator_repl(): # pragma: no cover
    # REPL Implementation
    """CLI for calculator."""
    try:
        calc = Calculator()
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))
        print("Calculator started. Type 'help' for commands.")
        while True:
            try:
                command = input("\nEnter command: ").lower().strip()
                if command == 'help':
      ...
                if command == 'exit':
                    try:
                        calc.save_history()
                        print("History saved successfully.")
                    except Exception as e:
                        print(f"Warning: Could not save history: {e}")
                    print("Goodbye!")
                    break
                if command == 'history':
                    history = calc.show_history()
                    if not history:
                        print("No calculations in history")
                    else:
                        print("\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            print(f"{i}. {entry}")
                    continue
     ... 
```
   - EAFP (From calculator_operations.py (Line 33 - 55))
```python
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
...
```
   - LBYL (From calculator_operations.py (Line 57 - 75))
```python
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
...
```
   - Logging (Panda code from calculator.py (Line 147 - 167))
```python
    def save_history(self) -> None:
        """Panda implementation, save calc history to CSV."""
        try:
            self.config.history_dir.mkdir(parents=True, exist_ok=True)
            history_data = []
            for calc in self.history:
                history_data.append({
                    'operation': str(calc.operation),
                    'operand1': str(calc.operand1),
                    'operand2': str(calc.operand2),
                    'result': str(calc.result),
                    'timestamp': calc.timestamp.isoformat()
                })
            if history_data:
                df = pd.DataFrame(history_data)
                df.to_csv(self.config.history_file, index=False)
                logging.info(f"History saved successfully to {self.config.history_file}")
            else:
                pd.DataFrame(columns=['operation', 'operand1', 'operand2', 'result', 'timestamp']
                           ).to_csv(self.config.history_file, index=False)
                logging.info("Empty history saved")
...
```
   - Logging Output Example
```
2024-11-08 19:05:31,059 - INFO - Logging initialized at: /home/mike/Projects/MidtermIS218/logs
2024-11-08 19:05:31,059 - INFO - No history file found - starting with empty history
2024-11-08 19:05:31,059 - INFO - Calculator initialized with configuration
2024-11-08 19:05:31,059 - INFO - Added observer: LoggingObserver
2024-11-08 19:05:31,059 - INFO - Added observer: AutoSaveObserver
2024-11-08 19:05:52,233 - INFO - Set operation: Addition
2024-11-08 19:05:52,233 - INFO - Calculation performed: Addition (5, 3) = 8
2024-11-08 19:05:52,240 - INFO - History saved successfully to /home/mike/Projects/MidtermIS218/history.csv
...
```
   - History (from calculator.py (Line 161 - 163))
```python
                df = pd.DataFrame(history_data)
                df.to_csv(self.config.history_file, index=False)
                logging.info(f"History saved successfully to {self.config.history_file}")
```
   - History Output Example
```
operation,operand1,operand2,result,timestamp
Addition,5,3,8,2024-11-08T19:05:52.233295
Subtraction,10,2,8,2024-11-08T19:05:57.526414
Root,2,2,1.4142135623730951454746218587388284504413604736328125,2024-11-08T19:06:06.393567
Power,5,2,25,2024-11-08T19:06:12.077431
Multiplication,2,2,4,2024-11-08T19:06:18.093209
Division,2,2,1,2024-11-08T19:06:21.957733
...
```

## Environment Configuration

Variables stored within a .env file that are loaded into the code in:
calculator_config.py (Line 34 - 39)
```python
        """Initalizing config wiht .env varibles and/or defaults."""
        # Set base directory to project root by default
        project_root = get_project_root()
        self.base_dir = base_dir or Path(
            os.getenv('CALCULATOR_BASE_DIR', str(project_root))
        ).resolve()
...
```
(Line 41 - 44)
```python
        # Max history size
        self.max_history_size = max_history_size if max_history_size is not None else int(
            os.getenv('CALCULATOR_MAX_HISTORY_SIZE', '1000')
        )
...
```
(Line 46 - 50)
```python
        # Auto save On/Off
        auto_save_env = os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower()
        self.auto_save = auto_save if auto_save is not None else (
            auto_save_env == 'true' or auto_save_env == '1'
        )
...
```
(Line 52 - 55)
```python
        # Precision decimal point
        self.precision = precision if precision is not None else int(
            os.getenv('CALCULATOR_PRECISION', '10')
        )
...
```
(Line 57 - 60)
```python
        # Max input value
        self.max_input_value = max_input_value if max_input_value is not None else Decimal(
            os.getenv('CALCULATOR_MAX_INPUT_VALUE', '1e999')
        )
...
```
(Line 62 - 65)
```python
        # Default encoding
        self.default_encoding = default_encoding or os.getenv(
            'CALCULATOR_DEFAULT_ENCODING', 'utf-8'
        )
...
```

- `CALCULATOR_BASE_DIR`: Base directory for saving logs and history files.
- `CALCULATOR_MAX_HISTORY_SIZE`: Maximum size of the calculation history.
- `CALCULATOR_AUTO_SAVE`: Automatically save history after each operation.
- `CALCULATOR_PRECISION`: Decimal precision of results.
- `CALCULATOR_MAX_INPUT_VALUE`: Maximum allowable input value.
- `CALCULATOR_DEFAULT_ENCODING`: Default encoding for files.

## Testing

To run the unit tests for this calculator:

```bash
pytest --pylint --coverage
```
