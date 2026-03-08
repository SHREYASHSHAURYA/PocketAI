import re
import math


SAFE_GLOBALS = {
    "__builtins__": {},
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "pi": math.pi
}


def normalize_language(text):

    t = text.lower()

    t = re.sub(r"square root of\s+(\d+)", r"sqrt(\1)", t)
    t = re.sub(r"cube root of\s+(\d+)", r"(\1)**(1/3)", t)
    t = re.sub(r"cube of\s+(\d+)", r"(\1)**3", t)

    t = re.sub(r"(\d+)\s+to the power of\s+(\d+)", r"(\1)**(\2)", t)
    t = re.sub(r"power of\s+(\d+)\s+(\d+)", r"(\1)**(\2)", t)

    t = re.sub(r"\bplus\b", "+", t)
    t = re.sub(r"\bminus\b", "-", t)
    t = re.sub(r"\btimes\b", "*", t)
    t = re.sub(r"\bmultiplied by\b", "*", t)
    t = re.sub(r"\bdivided by\b", "/", t)

    t = re.sub(r"\bwhat is\b", "", t)
    t = re.sub(r"\bcalculate\b", "", t)

    return t


def calculate(expression):

    try:
        expression = normalize_language(expression)
        expression = expression.strip()

        if not expression:
            return None

        expression = expression.replace("^", "**")

        expression = re.sub(r"\b0+(\d+)\b", r"\1", expression)

        result = eval(expression, SAFE_GLOBALS)

        return f"{expression} = {result}"

    except Exception:
        return None


def extract_expression(text):

    normalized = normalize_language(text)

    if normalized.startswith("calculate"):
        candidate = normalized.replace("calculate", "", 1).strip()
        if candidate:
            return candidate

    func_match = re.search(r"(sqrt|sin|cos|tan|log)\s*\([^\)]*\)", normalized)
    if func_match:
        return func_match.group()

    power_match = re.search(r"\([^\)]*\)\*\*\([^\)]*\)", normalized)
    if power_match:
        return power_match.group()

    times_match = re.search(r"(\d+)\s+(times|multiplied by)\s+(\d+)", normalized)
    if times_match:
        return f"{times_match.group(1)}*{times_match.group(3)}"

    divide_match = re.search(r"(divide|divided)\s+(\d+)\s+by\s+(\d+)", normalized)
    if divide_match:
        return f"{divide_match.group(2)}/{divide_match.group(3)}"

    add_match = re.search(r"(add)\s+(\d+)\s+and\s+(\d+)", normalized)
    if add_match:
        return f"{add_match.group(2)}+{add_match.group(3)}"

    subtract_match = re.search(r"(subtract)\s+(\d+)\s+from\s+(\d+)", normalized)
    if subtract_match:
        return f"{subtract_match.group(3)}-{subtract_match.group(2)}"

    percent_of_match = re.search(r"(\d+)\s*(percent|%)\s*of\s*(\d+)", normalized)
    if percent_of_match:
        return f"({percent_of_match.group(1)}/100)*{percent_of_match.group(3)}"

    percent_more_match = re.search(r"(\d+)\s*(percent|%)\s+more\s+than\s+(\d+)", normalized)
    if percent_more_match:
        return f"{percent_more_match.group(3)}*(1+{percent_more_match.group(1)}/100)"

    percent_less_match = re.search(r"(\d+)\s*(percent|%)\s+less\s+than\s+(\d+)", normalized)
    if percent_less_match:
        return f"{percent_less_match.group(3)}*(1-{percent_less_match.group(1)}/100)"

    increase_match = re.search(r"increase\s+(\d+)\s+by\s+(\d+)\s*(percent|%)", normalized)
    if increase_match:
        return f"{increase_match.group(1)}*(1+{increase_match.group(2)}/100)"

    decrease_match = re.search(r"decrease\s+(\d+)\s+by\s+(\d+)\s*(percent|%)", normalized)
    if decrease_match:
        return f"{decrease_match.group(1)}*(1-{decrease_match.group(2)}/100)"

    percent_symbol_match = re.search(r"(\d+)%\s*of\s*(\d+)", normalized)
    if percent_symbol_match:
        return f"({percent_symbol_match.group(1)}/100)*{percent_symbol_match.group(2)}"

    average_match = re.search(r"average of ([0-9,\s]+)", normalized)
    if average_match:
        nums = average_match.group(1)
        values = [n.strip() for n in nums.split(",") if n.strip()]
        return f"({'+'.join(values)})/{len(values)}"

    sum_match = re.search(r"sum of ([0-9,\s]+)", normalized)
    if sum_match:
        nums = sum_match.group(1)
        values = [n.strip() for n in nums.split(",") if n.strip()]
        return "+".join(values)

    match = re.search(r"[0-9\.\+\-\*\/\^\(\) ]+", normalized)

    if match:
        expr = match.group().strip()

        if expr and re.search(r"[\+\-\*\/\^]", expr):
            return expr

    return None