# Valid EXAMPLE

states = {q0,q1,qaccept,qreject}
input_alphabet = {0,1}
tape_alphabet = {0,1,B}
blank = B
start = q0
accept = qaccept
reject = qreject

(q0, 1) -> (q1, 1, R)
(q1, 0) -> (q1, 0, R)
(q1, 1) -> (q1, 1, R)
(q1, B) -> (qaccept, B, R)

# INVALID EXAMPLE

# ERROR: as the machine is deterministic,so duplicate transitions are not allowed.
(q0, 1) -> (q1, X, R)
(q0, 1) -> (q2, X, L)

# ERROR: S is not allowed.
(q1, 0) -> (q2, 0, S)

# ERROR: Z is not in the tape alphabet.
(q1, Z) -> (q2, Z, R)