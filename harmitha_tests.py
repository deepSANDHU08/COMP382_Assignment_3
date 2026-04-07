import subprocess

print("Running tests...\n")

result = subprocess.run(["python3", "Pushpdeep/main.py"], capture_output=True, text=True)

if "TM loaded successfully" in result.stdout:
    print("Test 1 Passed")
else:
    print("Test 1 Failed")

if "States:" in result.stdout:
    print("Test 2 Passed")
else:
    print("Test 2 Failed")

if "Transitions:" in result.stdout:
    print("Test 3 Passed")
else:
    print("Test 3 Failed")