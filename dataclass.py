from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass
class TransitionAction:
    next_state: str
    write_symbol: str
    direction: str  # either 'L' or 'R

# Container for the Turing Machine 7 tuple.
# Member 1 defined the model, I'm defining how do we store it.

@dataclass
class TMData:

    states: List[str]                    # e.g. ['q0', 'q1', 'qaccept', 'qreject']
    input_alphabet: List[str]            # e.g. ['0', '1']
    tape_alphabet: List[str]             # e.g. ['0', '1', 'X', 'B']
    blank: str                           # must be 'B'
    start_state: str                     # usually 'q0'
    accept_state: str                    # 'qaccept'
    reject_state: str                    # 'qreject'

    # Transition format: (current_state, read_symbol) -> TransitionAction(next_state, write_symbol, direction)
    transitions: Dict[Tuple[str, str], TransitionAction] = field(default_factory=dict)