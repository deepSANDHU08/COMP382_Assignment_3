# TM Encoding Specification - Member 2

This document defines how we represent our deterministic single-tape Turing Machine with one tape head as a file.

# Syntax Rules
- Blank Symbol: Must be represented as `B`.
- State Names: Use `q0`, `q1`, `q2`, `qaccept`, and `qreject`
- Final States: The machine must have two halting states: `qaccept` and `qreject`.
- Movement: Only `L` (Left) or `R` (Right) are allowed.

# TRANSITION FORMAT

Each transition must be written as:
(current_state, read_symbol) -> (next_state, write_symbol, direction)
where direction is either:
L = move left
R = move right

For Example:
(q0, 1) -> (q1, X, R)

