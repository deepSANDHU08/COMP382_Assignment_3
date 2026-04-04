from typing import Dict, List, Tuple
from tm_data import TMData, TransitionAction


def parse_list(value: str) -> List[str]:
    parts = value.split(',')
    return [part.strip() for part in parts if part.strip()]

def parse_transition_line(line: str) -> Tuple[Tuple[str, str], TransitionAction]:
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
    action = TransitionAction(next_state=next_state, write_symbol=write_symbol, direction=direction)
    return key, action

def validate_tm(tm: TMData) -> None:
    # Check special states
    if tm.start_state not in tm.states:
        raise ValueError(f"Start state '{tm.start_state}' is not in states.")

    if tm.accept_state not in tm.states:
        raise ValueError(f"Accept state '{tm.accept_state}' is not in states.")

    if tm.reject_state not in tm.states:
        raise ValueError(f"Reject state '{tm.reject_state}' is not in states.")

    # Check blank symbol
    if tm.blank not in tm.tape_alphabet:
        raise ValueError(f"Blank symbol '{tm.blank}' is not in tape alphabet.")

    # Check input alphabet symbols are inside tape alphabet
    for symbol in tm.input_alphabet:
        if symbol not in tm.tape_alphabet:
            raise ValueError(f"Input symbol '{symbol}' is not in tape alphabet.")

    # Check transitions
    for (current_state, read_symbol), action in tm.transitions.items():
        if current_state not in tm.states:
            raise ValueError(f"Unknown current state '{current_state}' in transitions.")

        if read_symbol not in tm.tape_alphabet:
            raise ValueError(f"Read symbol '{read_symbol}' is not in tape alphabet.")

        if action.next_state not in tm.states:
            raise ValueError(f"Next state '{action.next_state}' is not in states.")

        if action.write_symbol not in tm.tape_alphabet:
            raise ValueError(f"Write symbol '{action.write_symbol}' is not in tape alphabet.")

        if action.direction not in ("L", "R"):
            raise ValueError(f"Invalid direction '{action.direction}' in transitions.")

def parse_tm_file(file_path: str) -> TMData:
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        # Remove empty lines and comment lines
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        cleaned_lines.append(line)

    fields = {}
    transitions: Dict[Tuple[str, str], TransitionAction] = {}

    in_transitions = False

    for line in cleaned_lines:
        if line.lower() == "transitions:":
            in_transitions = True
            continue

        if not in_transitions:
            if ":" not in line:
                raise ValueError(f"Invalid line before transitions: {line}")

            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()
            fields[key] = value
        else:
            # Parse each transition line
            key, action = parse_transition_line(line)
            if key in transitions:
                raise ValueError(f"Duplicate transition for {key} - machine must be deterministic.")
            transitions[key] = action

    # Build TMData from the parsed fields
    tm = TMData(
        states=parse_list(fields["states"]),
        input_alphabet=parse_list(fields["input_alphabet"]),
        tape_alphabet=parse_list(fields["tape_alphabet"]),
        blank=fields["blank"],
        start_state=fields["start"],
        accept_state=fields["accept"],
        reject_state=fields["reject"],
        transitions=transitions
    )

    validate_tm(tm)
    return tm
