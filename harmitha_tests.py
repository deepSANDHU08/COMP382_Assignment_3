import subprocess

def run_test(name, command, expected):
    print("\nRunning Test:", name)

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    output = result.stdout + result.stderr

    if expected in output:
        print("✅ Passed")
    else:
        print("❌ Failed")
        print("Output:")
        print(output)


# TEST 1
run_test(
    "Valid TM Parsing",
    ["python3", "Pushpdeep/main.py"],
    "TM loaded successfully"
)

# TEST 2
run_test(
    "Check States Output",
    ["python3", "Pushpdeep/main.py"],
    "States:"
)

# TEST 3
run_test(
    "Check Transitions",
    ["python3", "Pushpdeep/main.py"],
    "Transitions:"
)

# TEST 4
run_test(
    "Invalid File Test",
    ["python3", "Pushpdeep/main.py", "wrong.tm"],
    "Error"
)
