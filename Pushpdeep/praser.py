from typing import Dict, List, Tuple
from Pushpdeep.tm_data import TMData, TrasitionAction

def parse_list(vlaue: str) -> List[str]:
    parts = vlaue.split(',')
    return [part.strip() for part in parts if part.strip()]

def parse_transition_line(line: str) -> Tuple[Tuple[str, str], TrasitionAction]:
    # Expected format: current_state, read_symbol -> next_state, write_symbol, direction
    #Example line: 
    # q0, 1 -> q1,X,R

    if "->" not in line:
        raise ValueError(f"Invalid transition format: {line}")
    left, right = line.split("->")
    left = left.strip()
    right = right.strip()

    left_parts = [part.strip() for part in left.split(",")]
    right_parts = [part.strip() for part in right.split(",")]

    current_state, read_symbol = left_parts
    next_state, write_symbol, direction = right_parts

    if direction not in ('L', 'R'):
        raise ValueError(f"Invalid direction: {direction} in line: {line}")
    
    key = (current_state, read_symbol)
    action = TrasitionAction(next_state=next_state, write_symbol=write_symbol, direction=direction)
    return key, action