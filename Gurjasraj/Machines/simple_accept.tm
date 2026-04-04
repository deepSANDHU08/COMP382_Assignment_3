# simple_accept.tm — Accepts if first symbol is 1
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
