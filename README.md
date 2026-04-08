# COMP 382 Assignment 3: Turing Machine Parser, Simulator, and Pi Generator

This project builds a small Turing Machine toolkit in Python. The repository can:

- parse a `.tm` machine description into Python data structures
- validate that the machine definition is well formed
- simulate the machine step by step on a tape
- generate a Turing Machine that writes digits of pi
- verify the pi digits with `mpmath` when that library is installed

## How the Project Fits Together

The project flow is:

1. A `.tm` file is read by the parser.
2. The parser converts it into a `TMData` object.
3. The simulator runs that machine on an input tape.
4. For the pi task, `pi_algorithm.py` first computes digits of pi, then generates a `.tm` file that the simulator can run.
5. `main.py` acts as the single command-line entry point that ties these pieces together.

## What Each Python File Does

### `main.py`

This is the main runner for the whole project.

It:

- provides the command-line interface
- chooses between simulator mode and pi-algorithm mode
- loads built-in machine presets such as `accept`, `reject`, `binary`, and `pi`
- calls the parser to load `.tm` files
- calls the simulator to execute machines
- calls the pi generator to build `pi_calculator.tm`

If you want one file that represents the whole project workflow, this is it.

### `Pushpdeep/parser.py`

This file is the parser for `.tm` machine descriptions.

It:

- reads a Turing Machine file
- ignores blank lines and comment lines
- parses machine fields such as states, alphabets, blank symbol, and halting states
- parses each transition line in the form `q0,1 -> q1,X,R`
- checks for duplicate transitions
- validates the final machine before it is used by the simulator

This file is responsible for turning text into a valid in-memory machine.

### `Pushpdeep/tm_data.py`

This file defines the shared data structures used by the parser and simulator.

It contains:

- `TransitionAction`: one transition's result
- `TMData`: the full Turing Machine definition

`TMData` stores the machine's states, alphabets, special states, and transition table. In practice, this is the central data model for the project.

### `Gurjasraj/simulator.py`

This file is the Turing Machine execution engine.

It:

- defines the `Tape` class
- defines the `TMSimulator` class
- loads the input string onto the tape
- reads and writes tape symbols
- moves the head left or right
- follows the transition table one step at a time
- stops on accept, reject, missing transition, or max-step limit
- records an execution trace for debugging

This is the file that actually runs a Turing Machine after parsing.

### `Gurjasraj/pi_algorithm.py`

This file handles the pi-specific part of the assignment.

It:

- computes digits of pi using a spigot algorithm
- optionally verifies those digits with `mpmath`
- generates a `.tm` file that writes pi to `n` decimal places

So this file does not simulate a machine directly. Instead, it creates a machine description that can later be simulated by `simulator.py`.

### `dataclass.py`

This file also defines `TransitionAction` and `TMData`.

It appears to be an older or duplicate version of the shared data model. The active parser and simulator import `Pushpdeep/tm_data.py`, so that file is the one currently used in the working project flow.

### `harmitha_tests.py`

This is a simple script that runs another Python program with `subprocess` and checks whether some expected text appears in the output.

Its purpose is basic output-based testing rather than full unit testing.

### `test_pushpdeep.py`

This is a `pytest`-style test file.

It:

- runs a Python script with `subprocess`
- checks that the program exits successfully
- checks that key parser output fields appear

Like `harmitha_tests.py`, it is meant to test visible command-line behavior.

## Machine Files

The project also includes example machine descriptions in `Gurjasraj/Machines/`:

- `simple_accept.tm`: accepts `1` and rejects `0`
- `binary_increment.tm`: sample binary machine
- `pi_calculator.tm`: generated pi machine

## TM File Format

The simulator expects a deterministic single-tape machine with:

- `states`
- `input_alphabet`
- `tape_alphabet`
- `blank`
- `start`
- `accept`
- `reject`
- `transitions`

Example:

```text
states: q0,q1,qaccept,qreject
input_alphabet: 0,1
tape_alphabet: 0,1,X,B
blank: B
start: q0
accept: qaccept
reject: qreject
transitions:
q0,1 -> q1,X,R
q0,0 -> qreject,0,R
q1,B -> qaccept,B,R
```

Each transition must follow:

```text
current_state,current_symbol -> next_state,write_symbol,direction
```

The direction must be `L` or `R`, and each `(state, symbol)` pair can appear only once.

## How to Run the Project

Run a built-in machine:

```bash
python main.py --machine accept
python main.py --machine binary --input 101
```

Run a specific `.tm` file:

```bash
python main.py --tm-file Gurjasraj/Machines/simple_accept.tm --input 1
```

Print the execution trace:

```bash
python main.py --machine accept --trace
```

Generate the pi machine:

```bash
python main.py --mode pi-algorithm --pi-digits 5
```

Generate and then simulate the pi preset:

```bash
python main.py --machine pi --pi-digits 5
```

## Libraries, Versions, and Licenses

The Python files in this repository use the following libraries:

| Library | Where it is used | Version | License |
| --- | --- | --- | --- |
| Python | Entire project runtime | `3.12.10` in the current local environment | PSF License |
| `argparse` | `main.py`, `Gurjasraj/pi_algorithm.py`, `Gurjasraj/simulator.py` | Standard library module shipped with Python `3.12.10` | PSF License |
| `pathlib` | `main.py`, `Pushpdeep/parser.py`, `Gurjasraj/pi_algorithm.py`, `Gurjasraj/simulator.py` | Standard library module shipped with Python `3.12.10` | PSF License |
| `sys` | `main.py`, `Pushpdeep/parser.py`, `Gurjasraj/simulator.py` | Standard library module shipped with Python `3.12.10` | PSF License |
| `typing` | `dataclass.py`, `Pushpdeep/tm_data.py`, `Pushpdeep/parser.py`, `Gurjasraj/simulator.py` | Standard library module shipped with Python `3.12.10` | PSF License |
| `dataclasses` | `dataclass.py`, `Pushpdeep/tm_data.py` | Standard library module shipped with Python `3.12.10` | PSF License |
| `collections` | `Gurjasraj/simulator.py` uses `defaultdict` | Standard library module shipped with Python `3.12.10` | PSF License |
| `subprocess` | `harmitha_tests.py`, `test_pushpdeep.py` | Standard library module shipped with Python `3.12.10` | PSF License |
| `mpmath` | Optional verification in `Gurjasraj/pi_algorithm.py` | Not installed in the current local environment | BSD license |

Notes:
- `mpmath` is optional. The pi generator still runs without it, but digit verification is skipped if it is not installed.

## References
- Neso Academy. (n.d.). Turing machine - Introduction (Part 1) [Video]. YouTube. https://www.youtube.com/watch?v=PvLaPKPzq2I
- Neso Academy. (n.d.). Turing machine - Introduction (Part 2) [Video]. YouTube. https://www.youtube.com/watch?v=GPSk9tRsK2I
- Neso Academy. (n.d.). Turing machine (Formal definition) [Video]. YouTube. https://www.youtube.com/watch?v=yFEdBR-rP9g
- Neso Academy. (n.d.). Turing machine (Example 1) [Video]. YouTube. https://www.youtube.com/watch?v=D9eF_B8URnw
- Neso Academy. (n.d.). Turing machine (Example 2) [Video]. YouTube. https://www.youtube.com/watch?v=cR4Re0YfoOo
- Rabinowitz, S., & Wagon, S. (1995). A spigot algorithm for the digits of pi. The American Mathematical Monthly, 102(3), 195–203.
- Polymath Unlimited. (n.d.). A MILLION digits of Pi with 77 lines of code (Pi-day Special) [Video]. YouTube. https://www.youtube.com/watch?v=Y2EKdbVVH4o

## Summary

In the full project:

- `parser.py` reads and validates machine descriptions
- `tm_data.py` stores the machine in Python objects
- `simulator.py` executes the machine
- `pi_algorithm.py` creates a pi-specific machine
- `main.py` connects everything into one runnable program

## Bonus

As a bonus addition, the project also includes a web-based Turing Machine interface in `Gurjasraj/tm_simulator_gui.html`.

This was made as a webpage version of the simulator idea so the project can also be presented through a browser-based GUI, not only through Python command-line scripts.

## Vlog

For the current project, the deterministic single-tape format above is enough.

## Testing and Validation

The system was tested using both valid and invalid Turing Machine inputs.

- Verified that the parser correctly loads TM components such as states, alphabets, and transitions.
- Checked that invalid inputs produce appropriate error messages.
- Implemented automated test cases in Python to validate the functionality of `main.py` and parser logic.
- Used subprocess-based testing to run the program and verify output.

Screenshots of successful execution have been added as proof.

## References

Python Software Foundation. (n.d.). *unittest — Unit testing framework*. https://docs.python.org/3/library/unittest.html

Corey Schafer. (2019, July 24). *Python tutorial: Calling external commands using the subprocess module* [Video]. YouTube. https://www.youtube.com/watch?v=2Fp1N6dof0Y

ProgrammingKnowledge. (n.d.). *Python unit testing tutorial* [Video]. YouTube. https://www.youtube.com/watch?v=6tNS--WetLI

Vlog of Jang: https://drive.google.com/file/d/1EGtaC6TZnZOiMsCeG1nlmsicSlw_G9bi/view?usp=drive_link
