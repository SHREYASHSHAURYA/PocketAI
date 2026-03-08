from tools.calculator import calculate, extract_expression
from tools.python_executor import run_python


TOOLS = {
    "python": run_python,
}


def try_tool(user_input):

    text = user_input.lower().strip()

    if text.startswith("run python"):
        code = user_input[len("run python"):].strip()
        return run_python(code)

    expression = extract_expression(user_input)

    if expression:
        result = calculate(expression)

        if result:
            return result

    return None
