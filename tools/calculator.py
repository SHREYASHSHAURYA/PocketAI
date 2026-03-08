def calculate(expression):
    try:
        expression=expression.strip()
        result = eval(expression)
        return str(result)
    except Exception:
        return "Invalid calculation"





