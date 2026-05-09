import os
import subprocess

FILE_NAME = "test_code.py"


# =========================
# CREATE SAMPLE FILE
# =========================

def create_test_file():

    # Intentional error
    code = 'pritn("Hello World")'

    with open(FILE_NAME, "w") as f:
        f.write(code)

    print("\nTest file created with error.\n")


# =========================
# RUN PYTHON FILE
# =========================

def run_code():

    print("\nRunning code...\n")

    result = subprocess.run(
        ["python", FILE_NAME],
        capture_output=True,
        text=True
    )

    return result


# =========================
# AUTO FIX ERRORS
# =========================

def auto_fix():

    with open(FILE_NAME, "r") as f:
        code = f.read()

    # Fix typo
    code = code.replace("pritn", "print")

    with open(FILE_NAME, "w") as f:
        f.write(code)

    print("\nError fixed automatically.\n")


# =========================
# MAIN PIPELINE
# =========================

def pipeline():

    print("==============================")
    print("SELF-HEALING CI/CD PIPELINE")
    print("==============================")

    create_test_file()

    result = run_code()

    # IF ERROR
    if result.returncode != 0:

        print("Build Failed\n")
        print(result.stderr)

        auto_fix()

        print("\nRe-running after fix...\n")

        second = run_code()

        if second.returncode == 0:
            print("Build Successful After Fix\n")
            print(second.stdout)

        else:
            print("Still failing")
            print(second.stderr)

    else:
        print("Build Successful")
        print(result.stdout)


# =========================
# START
# =========================

pipeline()