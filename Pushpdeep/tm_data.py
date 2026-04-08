from dataclasses import dataclass, field
from typing import Dict, List, Tuple



@dataclass
class TransitionAction:
    # Describes the effect of one transition in the machine.
    next_state: str
    write_symbol: str
    direction: str #'L' or 'R'

@dataclass
class TMData:
    # Stores the complete parsed Turing machine definition.
    states: List[str]
    input_alphabet: List[str]
    tape_alphabet: List[str]
    blank: str
    start_state: str
    accept_state: str
    reject_state: str
    # Maps (current_state, read_symbol) to the action the machine should take.
    transitions: Dict[Tuple[str, str], TransitionAction] = field(default_factory=dict)
