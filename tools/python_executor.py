import io
import contextlib


SAFE_BUILTINS = {
    "print": print,
    "range": range,
    "len": len,
    "int": int,
    "float": float,
    "str": str,
}


def run_python(code):

    output = io.StringIO()

    try:
        with contextlib.redirect_stdout(output):
            exec(code, {"__builtins__": SAFE_BUILTINS})

        result = output.getvalue()

        if result.strip():
            return result.strip()

        return "Code executed successfully."

    except Exception as e:
        return f"Python error: {e}"

