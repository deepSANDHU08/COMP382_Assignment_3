import subprocess

def test_main_runs():
    result = subprocess.run(
        ["python3", "Pushpdeep/main.py"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, "Program did not run successfully"
    assert "TM loaded successfully" in result.stdout


def test_states_present():
    result = subprocess.run(
        ["python3", "Pushpdeep/main.py"],
        capture_output=True,
        text=True
    )

    assert "States:" in result.stdout


def test_transitions_present():
    result = subprocess.run(
        ["python3", "Pushpdeep/main.py"],
        capture_output=True,
        text=True
    )

    assert "Transitions:" in result.stdout


def test_accept_state():
    result = subprocess.run(
        ["python3", "Pushpdeep/main.py"],
        capture_output=True,
        text=True
    )

    assert "Accept state:" in result.stdout


def test_reject_state():
    result = subprocess.run(
        ["python3", "Pushpdeep/main.py"],
        capture_output=True,
        text=True
    )

    assert "Reject state:" in result.stdout