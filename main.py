import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Gurjasraj.pi_algorithm import generate_pi_tm, spigot_pi, verify_pi_digits
from Gurjasraj.simulator import TMSimulator
from Pushpdeep.parser import parse_tm_file


MACHINE_PRESETS = {
    "accept": {
        "tm_file": PROJECT_ROOT / "Gurjasraj" / "Machines" / "simple_accept.tm",
        "input": "1",
    },
    "reject": {
        "tm_file": PROJECT_ROOT / "Gurjasraj" / "Machines" / "simple_accept.tm",
        "input": "0",
    },
    "binary": {
        "tm_file": PROJECT_ROOT / "Gurjasraj" / "Machines" / "binary_increment.tm",
        "input": "101",
    },
    "pi": {
        "tm_file": PROJECT_ROOT / "Gurjasraj" / "Machines" / "pi_calculator.tm",
        "input": "5",
    },
}


def resolve_run_target(machine: str, tm_file: str | None, input_string: str | None, pi_digits: int) -> tuple[Path, str]:
    if tm_file:
        resolved_file = Path(tm_file)
        if not resolved_file.is_absolute():
            resolved_file = (PROJECT_ROOT / resolved_file).resolve()
        resolved_input = input_string if input_string is not None else ""
        return resolved_file, resolved_input

    preset = MACHINE_PRESETS[machine]
    resolved_file = Path(preset["tm_file"])
    resolved_input = preset["input"] if input_string is None else input_string

    if machine == "pi":
        resolved_input = str(pi_digits) if input_string is None else input_string

    return resolved_file, resolved_input


def print_tm_summary(tm) -> None:
    print("TM loaded successfully.")
    print("States:", tm.states)
    print("Input alphabet:", tm.input_alphabet)
    print("Tape alphabet:", tm.tape_alphabet)
    print("Blank symbol:", tm.blank)
    print("Start state:", tm.start_state)
    print("Accept state:", tm.accept_state)
    print("Reject state:", tm.reject_state)
    print("Transition count:", len(tm.transitions))


def run_machine(tm_file: Path, input_string: str, trace: bool, max_steps: int) -> None:
    tm = parse_tm_file(str(tm_file))
    print_tm_summary(tm)

    print("\nRunning simulation...")
    sim = TMSimulator(tm, input_string=input_string, max_steps=max_steps)
    sim.run()
    result = sim.get_result()

    print("Machine file:", tm_file)
    print("Input:", input_string)
    print("Accepted:", result["accepted"])
    print("Halt reason:", result["halt_reason"])
    print("Steps:", result["steps"])
    print("Tape output:", result["tape_content"])

    if trace:
        print("\nExecution trace:")
        sim.print_trace()


def parse_only(tm_file: Path) -> None:
    tm = parse_tm_file(str(tm_file))
    print_tm_summary(tm)


def run_pi_algorithm(num_digits: int, output_path: Path | None) -> None:
    digits = spigot_pi(num_digits)
    pi_str = str(digits[0]) + "." + "".join(map(str, digits[1:num_digits + 1]))

    print(f"=== Spigot Algorithm: Computing pi to {num_digits} decimal places ===")
    print(f"Result: {pi_str}")

    print("\n=== Verification using mpmath API ===")
    verified = verify_pi_digits(digits, num_digits)
    print(f"Verified: {'YES' if verified else 'NO / SKIPPED'}")

    target_path = output_path or (PROJECT_ROOT / "Gurjasraj" / "Machines" / "pi_calculator.tm")
    print("\n=== Generating Turing Machine (.tm file) ===")
    generate_pi_tm(num_digits, str(target_path))
    print(f"\nTM file: {target_path}")


def main():
    arg_parser = argparse.ArgumentParser(
        description="Unified runner for the COMP 382 Turing Machine project."
    )
    arg_parser.add_argument(
        "--mode",
        choices=["simulate", "pi-algorithm"],
        default="simulate",
        help="Choose whether main.py runs the simulator flow or the pi algorithm flow."
    )
    arg_parser.add_argument(
        "--machine",
        choices=sorted(MACHINE_PRESETS.keys()),
        default="accept",
        help="Choose a built-in machine preset."
    )
    arg_parser.add_argument(
        "--tm-file",
        help="Run a specific .tm file instead of a preset."
    )
    arg_parser.add_argument(
        "--output",
        help="Output path for generated TM files."
    )
    arg_parser.add_argument(
        "--input",
        help="Input string to place on the tape."
    )
    arg_parser.add_argument(
        "--pi-digits",
        type=int,
        default=5,
        help="When running the pi preset, regenerate the pi machine for this many digits."
    )
    arg_parser.add_argument(
        "--trace",
        action="store_true",
        help="Print the full execution trace."
    )
    arg_parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Parse the machine and print its summary without running it."
    )
    arg_parser.add_argument(
        "--generate-only",
        action="store_true",
        help="Only generate the pi machine file when using the pi preset."
    )
    arg_parser.add_argument(
        "--max-steps",
        type=int,
        default=100_000,
        help="Maximum number of steps before forced halt."
    )
    args = arg_parser.parse_args()

    try:
        if args.mode == "pi-algorithm":
            output_path = None
            if args.output:
                output_path = Path(args.output)
                if not output_path.is_absolute():
                    output_path = (PROJECT_ROOT / output_path).resolve()
            run_pi_algorithm(args.pi_digits, output_path)
            return

        tm_file, input_string = resolve_run_target(
            machine=args.machine,
            tm_file=args.tm_file,
            input_string=args.input,
            pi_digits=args.pi_digits,
        )

        if args.machine == "pi" and args.tm_file is None:
            print(f"Generating pi machine for {args.pi_digits} digits...")
            generate_pi_tm(args.pi_digits, str(tm_file))
            print()

            if args.generate_only:
                print(f"Generated machine file: {tm_file}")
                return

        if args.summary_only:
            parse_only(tm_file)
            return

        run_machine(
            tm_file=tm_file,
            input_string=input_string,
            trace=args.trace,
            max_steps=args.max_steps,
        )

    except ValueError as e:
        print("Error while parsing or running TM:")
        print(e)
    except FileNotFoundError as e:
        print("File not found:")
        print(e)


if __name__ == "__main__":
    main()
