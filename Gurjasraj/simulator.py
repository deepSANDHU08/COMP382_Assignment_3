import argparse
from collections import defaultdict
from pathlib import Path
import sys
from typing import List, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Pushpdeep.parser import parse_tm_file
from Pushpdeep.tm_data import TMData, TransitionAction


class Tape:
    """
    Represents an infinite tape using a defaultdict.
    
    The tape extends infinitely in both directions. Any unvisited cell
    automatically contains the blank symbol. This avoids manual bounds
    checking or list resizing.
    """

    def __init__(self, blank: str):
        self.blank = blank
        self.cells = defaultdict(lambda: self.blank)

    def read(self, position: int) -> str:
        """Read the symbol at the given position."""
        return self.cells[position]

    def write(self, position: int, symbol: str) -> None:
        """Write a symbol at the given position."""
        self.cells[position] = symbol

    def load_input(self, input_string: str) -> None:
        """Load an input string onto the tape starting at position 0."""
        for i, ch in enumerate(input_string):
            self.cells[i] = ch

    def get_bounds(self) -> tuple:
        """Return (min_pos, max_pos) of non-blank cells, or (0, 0) if empty."""
        non_blank = [pos for pos, sym in self.cells.items() if sym != self.blank]
        if not non_blank:
            return (0, 0)
        return (min(non_blank), max(non_blank))

    def get_content(self) -> str:
        """Return the tape content as a string (non-blank region only)."""
        lo, hi = self.get_bounds()
        return "".join(self.cells[i] for i in range(lo, hi + 1))

    def __repr__(self) -> str:
        return f"Tape({self.get_content()!r})"


class TMSimulator:
    """
    Turing Machine Simulator — the execution engine.

    Takes a parsed TMData description and an input string, then simulates
    the machine step by step. Supports:
      - step-by-step execution (step method)
      - full run until halt (run method)
      - execution trace logging for debugging
      - configurable step limit to prevent infinite loops
    """

    def __init__(self, tm: TMData, input_string: str = "", max_steps: int = 100_000):
        """
        Initialize the simulator.

        Args:
            tm: The parsed Turing Machine description (7-tuple).
            input_string: The initial input to place on the tape.
            max_steps: Safety limit to prevent infinite loops.
        """
        self.tm = tm
        self.max_steps = max_steps

        # --- Tape setup ---
        self.tape = Tape(blank=tm.blank)
        self.tape.load_input(input_string)

        # --- Head position ---
        self.head: int = 0

        # --- Current state ---
        self.state: str = tm.start_state

        # --- Execution tracking ---
        self.steps: int = 0
        self.halted: bool = False
        self.accepted: Optional[bool] = None  # None = still running, True = accepted, False = rejected
        self.halt_reason: str = ""

        # --- Trace log (for debugging / rubric requirement) ---
        self.trace: List[str] = []

    # ------------------------------------------------------------------ #
    #                        CORE EXECUTION LOGIC                         #
    # ------------------------------------------------------------------ #

    def step(self) -> bool:
        """
        Execute a single step of the Turing Machine.

        One step consists of:
          1. Check if current state is a halting state
          2. Read the symbol under the tape head
          3. Look up the transition for (current_state, read_symbol)
          4. Write the new symbol to the tape
          5. Move the head left or right
          6. Update the current state

        Returns:
            True if the machine can continue (not halted).
            False if the machine has halted.
        """
        if self.halted:
            return False

        # Record the current configuration before executing
        self._record_trace()

        # --- Step 1: Check halting states ---
        if self.state == self.tm.accept_state:
            self.halted = True
            self.accepted = True
            self.halt_reason = f"Reached accept state '{self.tm.accept_state}'"
            return False

        if self.state == self.tm.reject_state:
            self.halted = True
            self.accepted = False
            self.halt_reason = f"Reached reject state '{self.tm.reject_state}'"
            return False

        # --- Step 2: Read symbol under head ---
        read_symbol = self.tape.read(self.head)

        # --- Step 3: Look up transition ---
        key = (self.state, read_symbol)
        if key not in self.tm.transitions:
            # No transition defined for this (state, symbol) pair
            # Machine halts and rejects (undefined transition = implicit reject)
            self.halted = True
            self.accepted = False
            self.halt_reason = f"No transition defined for ({self.state}, '{read_symbol}')"
            return False

        action: TransitionAction = self.tm.transitions[key]

        # --- Step 4: Write symbol ---
        self.tape.write(self.head, action.write_symbol)

        # --- Step 5: Move head ---
        if action.direction == "R":
            self.head += 1
        elif action.direction == "L":
            self.head -= 1

        # --- Step 6: Update state ---
        self.state = action.next_state

        # Increment step counter
        self.steps += 1

        return True

    def run(self) -> str:
        """
        Run the Turing Machine until it halts or exceeds max_steps.

        Returns:
            The tape content (non-blank region) after halting.
        """
        while self.steps < self.max_steps:
            if not self.step():
                break

        # Check if we hit the step limit without halting
        if not self.halted:
            self.halted = True
            self.accepted = False
            self.halt_reason = f"Exceeded maximum step limit ({self.max_steps})"

        # Record final configuration
        self._record_trace()

        return self.tape.get_content()

    # ------------------------------------------------------------------ #
    #                        TRACE / DEBUG LOGGING                        #
    # ------------------------------------------------------------------ #

    def _record_trace(self) -> str:
        """
        Record the current machine configuration as a human-readable string.
        
        Format: Step N: state=qX, head=H, tape=[...>sym<...]
        The > < markers show where the head is pointing.
        """
        lo, hi = self.tape.get_bounds()
        # Expand bounds to include head position
        lo = min(lo, self.head)
        hi = max(hi, self.head)

        # Build tape visualization with head marker
        tape_parts = []
        for i in range(lo, hi + 1):
            sym = self.tape.read(i)
            if i == self.head:
                tape_parts.append(f">{sym}<")
            else:
                tape_parts.append(f" {sym} ")

        tape_str = "".join(tape_parts)

        if self.halted:
            status = f"ACCEPTED" if self.accepted else f"REJECTED"
            entry = f"Step {self.steps:>4d}: [{self.state}] {tape_str}  --> {status}: {self.halt_reason}"
        else:
            entry = f"Step {self.steps:>4d}: [{self.state}] {tape_str}"

        self.trace.append(entry)
        return entry

    def get_trace(self) -> str:
        """Return the full execution trace as a single string."""
        return "\n".join(self.trace)

    def print_trace(self) -> None:
        """Print the full execution trace to stdout."""
        print(self.get_trace())

    # ------------------------------------------------------------------ #
    #                          STATUS / OUTPUT                            #
    # ------------------------------------------------------------------ #

    def get_result(self) -> dict:
        """
        Return a summary of the simulation result.
        Useful for testing and for the debug log.
        """
        return {
            "halted": self.halted,
            "accepted": self.accepted,
            "halt_reason": self.halt_reason,
            "steps": self.steps,
            "final_state": self.state,
            "tape_content": self.tape.get_content(),
            "head_position": self.head,
        }

    def __repr__(self) -> str:
        status = "running"
        if self.halted:
            status = "accepted" if self.accepted else "rejected"
        return (
            f"TMSimulator(state='{self.state}', head={self.head}, "
            f"steps={self.steps}, status={status})"
        )


# ---------------------------------------------------------------------- #
#                           COMMAND-LINE INTERFACE                        #
# ---------------------------------------------------------------------- #

def main():
    """
    Entry point for running the simulator from the command line.

    Usage:
        python simulator.py <tm_file> [input_string] [--trace] [--max-steps N]

    Examples:
        python simulator.py machines/binary_increment.tm 101 --trace
        python simulator.py machines/simple_accept.tm 1
        python simulator.py machines/pi_7.tm 7 --max-steps 500000
    """
    arg_parser = argparse.ArgumentParser(
        description="Turing Machine Simulator — executes a .tm file step by step."
    )
    arg_parser.add_argument(
        "tm_file",
        help="Path to the .tm file containing the TM description."
    )
    arg_parser.add_argument(
        "input",
        nargs="?",
        default="",
        help="Input string to place on the tape (default: empty)."
    )
    arg_parser.add_argument(
        "--trace",
        action="store_true",
        help="Print the full step-by-step execution trace."
    )
    arg_parser.add_argument(
        "--max-steps",
        type=int,
        default=100_000,
        help="Maximum number of steps before forced halt (default: 100000)."
    )

    args = arg_parser.parse_args()

    # --- Parse the TM file ---
    print(f"Loading TM from: {args.tm_file}")
    try:
        tm = parse_tm_file(args.tm_file)
    except ValueError as e:
        print(f"Error parsing TM file:\n  {e}")
        return
    except FileNotFoundError:
        print(f"File not found: {args.tm_file}")
        return

    print(f"  States: {len(tm.states)}, Transitions: {len(tm.transitions)}")
    print(f"  Start: {tm.start_state}, Accept: {tm.accept_state}, Reject: {tm.reject_state}")
    print(f"  Input string: '{args.input}'")
    print()

    # --- Run the simulator ---
    sim = TMSimulator(tm, input_string=args.input, max_steps=args.max_steps)
    result = sim.run()

    # --- Output results ---
    info = sim.get_result()

    if info["accepted"]:
        print(f"Result: ACCEPTED")
    else:
        print(f"Result: REJECTED")

    print(f"Halt reason: {info['halt_reason']}")
    print(f"Total steps: {info['steps']}")
    print(f"Final state: {info['final_state']}")
    print(f"Tape output: {info['tape_content']}")

    if args.trace:
        print(f"\n{'='*60}")
        print(f"EXECUTION TRACE ({info['steps']} steps)")
        print(f"{'='*60}")
        sim.print_trace()


if __name__ == "__main__":
    main()
