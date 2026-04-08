# Turing Machine Input Format for the Simulator

This document explains how a Turing Machine (TM) should be written so that the Python simulator can read it as an input string and execute it.

---

## Project Goal

The simulator should accept a TM description as input, parse it, and then simulate the machine step by step. This makes the simulator behave like a simple **Universal Turing Machine**.

For this project, one TM description will be used to compute an approximation of **pi to *n* decimal places**.

---

## Machine Model

The simulator assumes the following TM model:

* **Deterministic** Turing Machine
* **Single tape**
* **One tape head**
* Head can move only:

  * `L` = left
  * `R` = right
* Two halting states:

  * `qaccept`
  * `qreject`

---

## Required TM Components

Each TM description should include these parts:

1. **States**
2. **Input alphabet**
3. **Tape alphabet**
4. **Blank symbol**
5. **Start state**
6. **Accept state**
7. **Reject state**
8. **Transition rules**

---

## Recommended Text Format

A TM can be written in a simple structured text format like this:

```text
states: q0,q1,q2,qaccept,qreject
input_alphabet: 0,1
 tape_alphabet: 0,1,X,B
blank: B
start: q0
accept: qaccept
reject: qreject
transitions:
q0,1 -> q1,X,R
q0,0 -> qreject,0,R
q0,B -> qreject,B,R
q1,1 -> q1,1,R
q1,0 -> q2,0,L
q1,B -> qaccept,B,R
```

This format is easy to read and easy to parse in Python.

---

## Meaning of Each Section

### `states`

A comma-separated list of all states used by the machine.

Example:

```text
states: q0,q1,q2,qaccept,qreject
```

---

### `input_alphabet`

The symbols that are allowed in the original input.

Example:

```text
input_alphabet: 0,1
```

---

### `tape_alphabet`

The symbols that may appear on the tape while the TM is running.
This includes the input symbols plus any extra working symbols.

Example:

```text
tape_alphabet: 0,1,X,B
```

Here:

* `0` and `1` are input symbols
* `X` is a helper symbol
* `B` is the blank symbol

---

### `blank`

The character used for empty tape cells.

Example:

```text
blank: B
```

---

### `start`

The state where the TM begins execution.

Example:

```text
start: q0
```

---

### `accept` and `reject`

The halting states.

Example:

```text
accept: qaccept
reject: qreject
```

When the TM reaches one of these states, execution stops.

---

### `transitions`

The list of transition rules.

Each rule should follow this format:

```text
current_state,current_symbol -> next_state,write_symbol,move_direction
```

Example:

```text
q0,1 -> q1,X,R
```

This means:

* If the TM is in state `q0`
* and reads symbol `1`
* then it will:

  * move to state `q1`
  * write `X`
  * move the head to the right

---

## Transition Rule Template

General form:

```text
(q, a) -> (p, b, D)
```

Where:

* `q` = current state
* `a` = symbol currently being read
* `p` = next state
* `b` = symbol to write
* `D` = head movement (`L` or `R`)

Equivalent text form used by the simulator:

```text
q,a -> p,b,D
```

---

## Deterministic Rule Requirement

This simulator expects a **deterministic** TM.
That means:

* For each pair `(state, symbol)`
* there must be **at most one** transition rule

Example of valid deterministic rules:

```text
q0,0 -> q1,X,R
q0,1 -> q2,Y,L
```

Invalid example:

```text
q0,1 -> q1,X,R
q0,1 -> q2,1,L
```

The second example is not allowed because the same `(state, symbol)` pair has two different transitions.

---

## Example 1: Very Simple TM

This TM accepts if the first symbol is `1` and rejects otherwise.

```text
states: q0,qaccept,qreject
input_alphabet: 0,1
 tape_alphabet: 0,1,B
blank: B
start: q0
accept: qaccept
reject: qreject
transitions:
q0,1 -> qaccept,1,R
q0,0 -> qreject,0,R
q0,B -> qreject,B,R
```

### How it works

* Input starts with `1` → accept
* Input starts with `0` → reject
* Empty input (`B`) → reject

---

## Example 2: Expected Structure for the Pi Machine

The TM for computing pi will be much larger, but it should still follow the same format.

High-level example:

```text
states: q0,qLoadN,qInit,qCalc1,qCalc2,qWrite,qLoop,qaccept,qreject
input_alphabet: 0,1,2,3,4,5,6,7,8,9
 tape_alphabet: 0,1,2,3,4,5,6,7,8,9,.,#,B,X,Y
blank: B
start: q0
accept: qaccept
reject: qreject
transitions:
q0,7 -> qLoadN,7,R
qLoadN,B -> qInit,#,L
...
```

The exact transitions will depend on the arithmetic method used to approximate pi.

---

## Input to the Pi Machine

For the pi TM, the input should represent the number of decimal places to compute.

Example:

```text
7
```

Meaning:

* compute pi to 7 decimal places

Possible output on the tape:

```text
3.1415926
```

or

```text
3.1415927
```

depending on whether the machine truncates or rounds.

---

## Suggested Design for the Simulator

The Python simulator should read the TM description and store it in a structure similar to this:

```python
transitions[(current_state, current_symbol)] = (next_state, write_symbol, move)
```

Example:

```python
transitions[("q0", "1")] = ("q1", "X", "R")
```

This makes it easy to:

* look up the current rule
* write to the tape
* move the head
* update the state

---

## Tape Behavior

The simulator should support:

* reading the symbol under the head
* writing a new symbol
* moving left or right
* expanding the tape when needed

A simple implementation can treat missing cells as blank (`B`).

---

## Halting Conditions

The machine stops when:

* the current state becomes `qaccept`, or
* the current state becomes `qreject`

It is also a good idea for the Python simulator to include:

* a maximum step limit

This helps prevent infinite loops during debugging.

---

## Good Formatting Rules for TM Files

To keep the parser simple, follow these rules:

* Use commas to separate symbols and states
* Use `->` for transitions
* Use one transition per line
* Keep state names consistent
* Use only one blank symbol
* Use only `L` or `R` for movement
* Do not repeat the same `(state, symbol)` pair

---

## Recommended File Extension

You can store TM descriptions in files like:

```text
simple.tm
pi_7.tm
```

Then the Python program can read the file contents as a string and simulate the machine.

---

## Summary

A valid TM description for this project should clearly define:

* the machine states
* alphabets
* blank symbol
* start/accept/reject states
* deterministic transition rules

The same format can be used for:

* small test machines
* larger machines such as the pi approximation TM

This allows one Python simulator to execute any TM description written in the required format.

---

## Possible Future Improvements

Later, the format could be extended to support:

* comments
* multi-character tape symbols
* optional stay move (`S`)
* multiple tapes
* machine metadata

For the current project, the deterministic single-tape format above is enough.

## Testing and Validation

The system was tested using both valid and invalid Turing Machine inputs.

- Verified that the parser correctly loads TM components such as states, alphabets, and transitions.
- Checked that invalid inputs produce appropriate error messages.
- Implemented automated test cases in Python to validate the functionality of `main.py` and parser logic.
- Used subprocess-based testing to run the program and verify output.

Screenshots of successful execution have been added as proof.

## References

GeeksforGeeks. (2020, August 14). *Getting started with unit testing in Python*. GeeksforGeeks. https://www.geeksforgeeks.org/python/python-unit-testing/

Python Software Foundation. (n.d.). *unittest — Unit testing framework*. https://docs.python.org/3/library/unittest.html

Corey Schafer. (2019, July 24). *Python tutorial: Calling external commands using the subprocess module* [Video]. YouTube. https://www.youtube.com/watch?v=2Fp1N6dof0Y

ProgrammingKnowledge. (n.d.). *Python unit testing tutorial* [Video]. YouTube. https://www.youtube.com/watch?v=6tNS--WetLI

