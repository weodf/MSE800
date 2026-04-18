import math


class Calculator:
    @staticmethod
    def parse_number(value: str):
        value = value.strip().replace(" ", "")

        # Complex number
        if "j" in value.lower():
            try:
                return complex(value)
            except ValueError:
                raise ValueError(f"Invalid complex number: {value}")

        # Integer
        try:
            if "." not in value:
                return int(value)
        except ValueError:
            pass

        # Float
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Invalid number: {value}")

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return a / b

    @staticmethod
    def modulo(a, b):
        if isinstance(a, complex) or isinstance(b, complex):
            raise TypeError("Modulo (%) is not supported for complex numbers.")
        if b == 0:
            raise ZeroDivisionError("Modulo by zero is not allowed.")
        return a % b

    @staticmethod
    def factorial(n):
        if isinstance(n, complex):
            raise TypeError("Factorial is not supported for complex numbers.")

        if isinstance(n, float):
            if not n.is_integer():
                raise ValueError("Factorial is only defined for integers.")
            n = int(n)

        if not isinstance(n, int):
            raise TypeError("Factorial is only supported for integers.")

        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers.")

        return math.factorial(n)

    @staticmethod
    def calculate(operator: str, a, b=None):
        if operator == "+":
            return Calculator.add(a, b)
        elif operator == "-":
            return Calculator.subtract(a, b)
        elif operator == "*":
            return Calculator.multiply(a, b)
        elif operator == "/":
            return Calculator.divide(a, b)
        elif operator == "%":
            return Calculator.modulo(a, b)
        elif operator == "!":
            return Calculator.factorial(a)
        else:
            raise ValueError(f"Unsupported operator: {operator}")


def main():
    print("Supported operators: +, -, *, /, %, !")
    print("Supports integers, floats, and complex numbers (example: 2+3j)")
    print("Type 'exit' to quit.\n")

    while True:
        operator = input("Enter operator: ").strip()

        if operator.lower() == "exit":
            print("End.")
            break

        try:
            if operator == "!":
                first = input("Enter a number: ").strip()
                if first.lower() == "exit":
                    print("End.")
                    break

                a = Calculator.parse_number(first)
                result = Calculator.calculate(operator, a)
                print(f"Result: {result}\n")

            elif operator in ["+", "-", "*", "/", "%"]:
                first = input("Enter first number: ").strip()
                if first.lower() == "exit":
                    print("End.")
                    break

                second = input("Enter second number: ").strip()
                if second.lower() == "exit":
                    print("End.")
                    break

                a = Calculator.parse_number(first)
                b = Calculator.parse_number(second)

                result = Calculator.calculate(operator, a, b)
                print(f"Result: {result}\n")

            else:
                print("Invalid operator. Please use +, -, *, /, %, !\n")

        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()