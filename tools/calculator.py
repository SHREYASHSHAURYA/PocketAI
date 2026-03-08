import re


def calculate(expression):

    try:
        expression = expression.strip()

        if not expression:
            return None

        result = eval(expression)

        return f"{expression} = {result}"

    except Exception:
        return None


def extract_expression(text):

    match = re.search(r"[0-9\.\+\-\*\/\(\) ]+", text)

    if match:
        return match.group().strip()

    return None




