import subprocess

print("Running Parser Test...")

try:
    result = subprocess.run(
        ["python3", "Pushpdeep/main.py"],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if "TM loaded successfully" in result.stdout:
        print("✅ Parser Test Passed")
    else:
        print("❌ Parser Test Failed")

except Exception as e:
    print("❌ Parser Test Error:", e)
