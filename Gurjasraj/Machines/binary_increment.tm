# binary_increment.tm — Adds 1 to a binary number
states: qRight,qCarry,qDone,qaccept,qreject
input_alphabet: 0,1
tape_alphabet: 0,1,B
blank: B
start: qRight
accept: qaccept
reject: qreject
transitions:
qRight,0 -> qRight,0,R
qRight,1 -> qRight,1,R
qRight,B -> qCarry,B,L
qCarry,1 -> qCarry,0,L
qCarry,0 -> qDone,1,L
qCarry,B -> qDone,1,R
qDone,0 -> qDone,0,L
qDone,1 -> qDone,1,L
qDone,B -> qaccept,B,R
