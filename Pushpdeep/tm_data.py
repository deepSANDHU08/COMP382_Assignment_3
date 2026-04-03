from dataclasses import dataclass


@dataclass
class TrasitionAction:
    next_state: str
    write_symbol: str
    direction: str #'L' or 'R'

@dataclass
class TMData:
    states: List[str]
    input_alphabet: List[str]
    tape_alphabet: List[str]
    blank: str
    initial_state: str
    accepting_states: List[str]
    rejecting_states: List[str]
    #key: (current_state, read_symbol)
    #Value: TransitionAction
    transitions: Dict[Tuple[str, str], TrasitionAction] = field(default_factory=dict)