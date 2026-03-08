from tools.calculator import calculate, extract_expression
from tools.python_executor import run_python
from tools.web_search import web_search


TOOLS = {
    "python": run_python,
}


def try_tool(user_input):

    text = user_input.lower().strip()

    if text.startswith("run python"):
        code = user_input[len("run python"):].strip()
        return run_python(code)

    if text.startswith("search"):
        query = user_input[len("search"):].strip()
        results = web_search(query)

        if results:
            return f"Web search results:\n\n{results}"

    if text.startswith("web search"):
        query = user_input[len("web search"):].strip()
        results = web_search(query)

        if results:
            return f"Web search results:\n\n{results}"

    expression = extract_expression(user_input)

    if expression:
        result = calculate(expression)

        if result:
            return result

    return None
