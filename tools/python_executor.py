import io
import contextlib

def run_python(code):
    output = io.StringIO()

    try:
        with contextlib.redirect_stdout(output):
            exec(code, {})
        return output.getvalue() if output.getvalue() else "Code executed."
    except Exception as e:
        return str(e)

