from tools.calculator import calculate
from tools.python_executor import run_python

def try_tool(user_input):

    text = user_input.lower()

    if text.startswith("calculate"):
        expression = user_input.replace("calculate", "").strip()
        return calculate(expression)

    if text.startswith("run python"):
        code = user_input.replace("run python", "").strip()
        return run_python(code)

    return None

