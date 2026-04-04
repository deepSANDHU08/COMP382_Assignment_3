from dataclasses import dataclass, field
from typing import Dict, List, Tuple



@dataclass
class TransitionAction:
    next_state: str
    write_symbol: str
    direction: str #'L' or 'R'

@dataclass
class TMData:
    states: List[str]
    input_alphabet: List[str]
    tape_alphabet: List[str]
    blank: str
    start_state: str
    accept_state: str
    reject_state: str
    #key: (current_state, read_symbol)
    #Value: TransitionAction
    transitions: Dict[Tuple[str, str], TransitionAction] = field(default_factory=dict)
