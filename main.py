from flask import Flask
import subprocess

app = Flask(__name__)

FILE_NAME = "test_code.py"


# =========================
# CREATE TEST FILE
# =========================

def create_test_file():

    code = 'pritn("Hello World")'

    with open(FILE_NAME, "w") as f:
        f.write(code)


# =========================
# RUN CODE
# =========================

def run_code():

    result = subprocess.run(
        ["python", FILE_NAME],
        capture_output=True,
        text=True
    )

    return result


# =========================
# AUTO FIX
# =========================

def auto_fix():

    with open(FILE_NAME, "r") as f:
        code = f.read()

    code = code.replace("pritn", "print")

    with open(FILE_NAME, "w") as f:
        f.write(code)


# =========================
# PIPELINE
# =========================

def pipeline():

    logs = ""

    logs += "SELF-HEALING CI/CD PIPELINE\n\n"

    create_test_file()

    result = run_code()

    if result.returncode != 0:

        logs += "Build Failed\n\n"
        logs += result.stderr + "\n"

        auto_fix()

        logs += "Error fixed automatically\n\n"

        second = run_code()

        if second.returncode == 0:

            logs += "Build Successful After Fix\n\n"
            logs += second.stdout

        else:

            logs += "Still failing\n"
            logs += second.stderr

    else:

        logs += "Build Successful\n"
        logs += result.stdout

    return logs


# =========================
# WEB ROUTES
# =========================

@app.route("/")
def home():

    return """
    <h1>Self-Healing CI/CD Pipeline</h1>

    <p>Project is running successfully.</p>

    <a href='/run'>Run Pipeline</a>
    """


@app.route("/run")
def run_pipeline():

    result = pipeline()

    return f"<pre>{result}</pre>"


# =========================
# START SERVER
# =========================

if __name__ == "__main__":

    import os

    # Running inside GitHub Actions
    if os.environ.get("GITHUB_ACTIONS") == "true":

        print(pipeline())

    # Running on Render/browser
    else:

        app.run(
            host="0.0.0.0",
            port=10000,
            debug=False
        )