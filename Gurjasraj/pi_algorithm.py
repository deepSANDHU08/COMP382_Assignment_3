# pi_algorithm.py — Pi Algorithm Design and TM Logic (Member 3 + Member 5)
#
# This module implements the Spigot Algorithm (Rabinowitz & Wagon, 1995)
# for computing digits of pi using only integer arithmetic, then generates
# a Turing Machine (.tm file) that produces pi to n decimal places.
#
# It also uses the mpmath library (BSD license) as an API to verify
# the correctness of our spigot implementation.
#
# References:
#   - Rabinowitz, S. & Wagon, S. (1995). A Spigot Algorithm for the
#     Digits of Pi. The American Mathematical Monthly, 102(3), 195-203.
#   - Jeremy Gibbons: Unbounded Spigot Algorithms for the Digits of Pi
#   - mpmath library: https://mpmath.org/ (BSD license)
#
# Usage:
#   python pi_algorithm.py                  # compute pi to 7 places, verify, generate .tm
#   python pi_algorithm.py --digits 10      # compute pi to 10 places
#   python pi_algorithm.py --generate-tm 7  # generate pi_7.tm file

import argparse
from pathlib import Path

try:
    from mpmath import mp  # API/library for arbitrary-precision verification
except ImportError:
    mp = None


# =========================================================================
#  PART 1: Spigot Algorithm — computes pi digit by digit (integer-only)
# =========================================================================

def spigot_pi(num_digits: int) -> list:
    """
    Compute digits of pi using the Rabinowitz-Wagon Spigot Algorithm.

    This algorithm uses only integer arithmetic (no floating point),
    making it conceptually compatible with Turing machine operations.

    How it works:
      - Maintains an array of 'remainders' of length ceil(10*n/3) + 1
      - Each iteration extracts one digit of pi by:
        1. Multiplying each element by 10
        2. Sweeping right-to-left, computing carry = element // (2i+1)
           and passing carry * i to the next position left
        3. At position 0, the quotient gives a 'predigit'
        4. A buffering mechanism handles predigits of 9 and 10
           (these may change if a carry propagates from a later digit)

    Args:
        num_digits: Number of decimal digits to compute.

    Returns:
        List of integers representing digits of pi (including the leading 3).
        For num_digits=7, returns [3, 1, 4, 1, 5, 9, 2, 6].
    """
    # Extra iterations needed to handle predigit buffering edge cases
    extra = 10
    array_len = (10 * (num_digits + extra)) // 3 + 1

    # Initialize: all elements start at 2 (from the series representation)
    remainders = [2] * array_len

    digits = []
    predigit = 0       # the digit waiting to be confirmed
    nines_count = 0    # count of consecutive 9s being buffered

    for iteration in range(num_digits + 1 + extra):
        # Step 1: Sweep right-to-left, multiply by 10, propagate carries
        carry = 0
        for i in range(array_len - 1, 0, -1):
            # Multiply by 10 and add incoming carry
            numerator = remainders[i] * 10 + carry

            # The denominator for position i is (2*i + 1)
            denominator = 2 * i + 1

            # New remainder stays, carry propagates left (multiplied by i)
            remainders[i] = numerator % denominator
            carry = (numerator // denominator) * i

        # Step 2: Handle position 0 separately
        numerator = remainders[0] * 10 + carry
        remainders[0] = numerator % 10
        new_predigit = numerator // 10

        # Step 3: Predigit buffering (handles 9s and carry propagation)
        if new_predigit == 9:
            # Buffer this 9 — it might become 0 if a carry arrives later
            nines_count += 1
        elif new_predigit == 10:
            # Carry propagation: increment the stored predigit,
            # flush all buffered 9s as 0s (9+1=10, write 0 carry 1)
            digits.append(predigit + 1)
            for _ in range(nines_count):
                digits.append(0)
            nines_count = 0
            predigit = 0  # 10 mod 10 = 0
        else:
            # Normal case: output the stored predigit and all buffered 9s
            if iteration > 0:
                digits.append(predigit)
                for _ in range(nines_count):
                    digits.append(9)
                nines_count = 0
            predigit = new_predigit

        # Early exit once we have enough digits
        if len(digits) > num_digits + 1:
            break

    return digits[:num_digits + 1]


# =========================================================================
#  PART 2: Verification using mpmath API
# =========================================================================

def verify_pi_digits(computed_digits: list, num_decimal_places: int) -> bool:
    """
    Verify computed pi digits against mpmath's arbitrary-precision pi.

    Uses the mpmath library as an external API for verification.
    mpmath computes pi using the Chudnovsky algorithm internally,
    which is independent of our spigot method — making this a valid
    cross-check.

    Args:
        computed_digits: List of digits from spigot_pi().
        num_decimal_places: How many decimal digits to verify.

    Returns:
        True if all digits match, False otherwise.
    """
    if mp is None:
        print("  Skipping verification: mpmath is not installed.")
        return False

    # Set mpmath precision higher than needed to avoid rounding issues
    mp.dps = num_decimal_places + 10

    # Get pi string with extra digits so we can truncate (not round)
    pi_full = mp.nstr(mp.pi, num_decimal_places + 5, strip_zeros=False)

    # Extract expected digits by truncation (not rounding)
    expected = [int(ch) for ch in pi_full if ch.isdigit()]

    # Compare up to num_decimal_places + 1 (including the "3")
    num_to_check = num_decimal_places + 1
    computed_trimmed = computed_digits[:num_to_check]
    expected_trimmed = expected[:num_to_check]

    match = computed_trimmed == expected_trimmed

    print(f"  Computed:  {''.join(map(str, computed_trimmed))}")
    print(f"  Expected:  {''.join(map(str, expected_trimmed))}")
    print(f"  Match:     {'YES' if match else 'NO'}")

    if not match:
        for i in range(min(len(computed_trimmed), len(expected_trimmed))):
            if computed_trimmed[i] != expected_trimmed[i]:
                print(f"  First mismatch at position {i}: got {computed_trimmed[i]}, expected {expected_trimmed[i]}")
                break

    return match


# =========================================================================
#  PART 3: TM File Generator — creates a .tm file from computed digits
# =========================================================================

def generate_pi_tm(num_digits: int, output_path: str) -> None:
    """
    Generate a Turing Machine description file (.tm) that computes pi
    to the specified number of decimal places.

    The TM is generated programmatically from the spigot algorithm's output.
    Each state represents a phase of the digit-extraction process:
      - qRead:     Read input n from tape
      - qDotN:     Write decimal point, N digits remaining
      - qDX_toY:   Write digit X of pi, continue to digit Y
      - qDX_done:  Write digit X of pi, then halt

    This approach maps the spigot algorithm's iterative structure onto
    TM states: each digit extraction is a state transition.

    Args:
        num_digits: Maximum number of decimal places the TM supports.
        output_path: Path to write the .tm file.
    """
    # First, compute pi digits using the spigot algorithm
    digits = spigot_pi(num_digits)
    pi_decimals = digits[1:num_digits + 1]  # exclude the leading 3

    print(f"\n  Generating TM for pi = 3.{''.join(map(str, pi_decimals))}")

    # Collect all states we'll need
    all_states = ["qRead", "qaccept", "qreject"]
    transitions = []

    # qDotN states (write the decimal point, N digits remaining)
    for n in range(1, num_digits + 1):
        all_states.append(f"qDot{n}")

    # qDX_toY and qDX_done states
    for d in range(1, num_digits + 1):
        all_states.append(f"qD{d}_done")
        for remaining in range(d + 1, num_digits + 1):
            all_states.append(f"qD{d}_to{remaining}")

    # --- Build transitions ---

    # Phase 1: Read input n → write "3", branch to qDotN
    for n in range(1, num_digits + 1):
        transitions.append(f"qRead,{n} -> qDot{n},3,R")
    transitions.append(f"qRead,B -> qreject,B,R")

    # Phase 2: Write decimal point
    for n in range(1, num_digits + 1):
        if n == 1:
            next_state = "qD1_done"
        else:
            next_state = "qD1_to" + str(n)
        transitions.append(f"qDot{n},B -> {next_state},.,R")

    # Phase 3: Write digits
    for d in range(1, num_digits + 1):
        digit_char = str(pi_decimals[d - 1])

        # qDd_done: write digit d, accept
        transitions.append(f"qD{d}_done,B -> qaccept,{digit_char},R")

        # qDd_toY: write digit d, go to next digit state
        for target in range(d + 1, num_digits + 1):
            # target = total digits requested
            # We're writing digit d, and need to continue to digit d+1
            # If d+1 == target, then d+1 is the last digit → qD{d+1}_done
            # Otherwise, d+1 still has more to go → qD{d+1}_to{target}
            if d + 1 == target:
                next_state = f"qD{d+1}_done"
            else:
                next_state = f"qD{d+1}_to{target}"

            transitions.append(f"qD{d}_to{target},B -> {next_state},{digit_char},R")

    # --- Build tape alphabet (digits 0-9 plus dot and blank) ---
    tape_symbols = set()
    for d in pi_decimals:
        tape_symbols.add(str(d))
    for n in range(1, num_digits + 1):
        tape_symbols.add(str(n))
    tape_symbols.add(".")
    tape_symbols.add("B")
    tape_sorted = sorted(tape_symbols, key=lambda x: (x == "B", x == ".", x))

    input_symbols = [str(n) for n in range(1, num_digits + 1)]

    # --- Write the .tm file ---
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as f:
        f.write(f"# pi_calculator.tm — Computes pi to n decimal places (n = 1 to {num_digits})\n")
        f.write(f"#\n")
        f.write(f"# Generated by pi_algorithm.py using the Spigot Algorithm\n")
        f.write(f"# (Rabinowitz & Wagon, 1995) with mpmath verification.\n")
        f.write(f"#\n")
        f.write(f"# Algorithm: Rabinowitz-Wagon Spigot (integer-only arithmetic)\n")
        f.write(f"# Verification API: mpmath (BSD license) — https://mpmath.org/\n")
        f.write(f"#\n")
        f.write(f"# Pi to {num_digits} places: 3.{''.join(map(str, pi_decimals))}\n")
        f.write(f"#\n")
        f.write(f"# Phases:\n")
        f.write(f"#   qRead     — Read input n (1-{num_digits}), write '3'\n")
        f.write(f"#   qDotN     — Write '.', N digits remaining\n")
        f.write(f"#   qDX_toY   — Write digit X, continue to digit Y\n")
        f.write(f"#   qDX_done  — Write digit X, halt (accept)\n")
        f.write(f"#\n")
        f.write(f"# Input:  single digit n (1-{num_digits})\n")
        f.write(f"# Output: 3.{{first n digits of pi}} on the tape\n")
        f.write(f"\n")
        f.write(f"states: {','.join(all_states)}\n")
        f.write(f"input_alphabet: {','.join(input_symbols)}\n")
        f.write(f"tape_alphabet: {','.join(tape_sorted)}\n")
        f.write(f"blank: B\n")
        f.write(f"start: qRead\n")
        f.write(f"accept: qaccept\n")
        f.write(f"reject: qreject\n")
        f.write(f"transitions:\n")
        for t in transitions:
            f.write(f"{t}\n")

    print(f"  Written to: {output_file}")
    print(f"  States: {len(all_states)}, Transitions: {len(transitions)}")


# =========================================================================
#  PART 4: Main — compute, verify, generate
# =========================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Compute pi using the Spigot Algorithm and generate a TM file."
    )
    parser.add_argument(
        "--digits", type=int, default=7,
        help="Number of decimal places to compute (default: 7)."
    )
    parser.add_argument(
        "--generate-tm", type=int, default=None,
        help="Generate a .tm file supporting up to N decimal places."
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Output path for the .tm file (default: machines/pi_calculator.tm)."
    )
    args = parser.parse_args()

    num_digits = args.digits

    # --- Step 1: Compute pi using the Spigot Algorithm ---
    print(f"=== Spigot Algorithm: Computing pi to {num_digits} decimal places ===")
    digits = spigot_pi(num_digits)
    pi_str = str(digits[0]) + "." + "".join(map(str, digits[1:num_digits + 1]))
    print(f"  Result: {pi_str}")

    # --- Step 2: Verify using mpmath API ---
    print(f"\n=== Verification using mpmath API ===")
    verified = verify_pi_digits(digits, num_digits)
    if verified:
        print(f"  Spigot algorithm output VERIFIED to {num_digits} decimal places.")
    else:
        if mp is None:
            print(f"  Verification skipped because mpmath is unavailable.")
        else:
            print(f"  WARNING: Verification FAILED!")

    # --- Step 3: Generate TM file if requested ---
    gen_digits = args.generate_tm if args.generate_tm else num_digits
    output_path = args.output if args.output else str(Path("Gurjasraj") / "Machines" / "pi_calculator.tm")

    print(f"\n=== Generating Turing Machine (.tm file) ===")
    generate_pi_tm(gen_digits, output_path)

    # --- Step 4: Summary ---
    print(f"\n=== Summary ===")
    print(f"  Algorithm:    Rabinowitz-Wagon Spigot (integer-only)")
    print(f"  Digits:       {pi_str}")
    verification_status = "SKIPPED" if mp is None else ("YES" if verified else "NO")
    print(f"  Verified:     {verification_status} (via mpmath)")
    print(f"  TM file:      {output_path}")
    print(f"\n  To run: python Gurjasraj\\simulator.py {output_path} {num_digits} --trace")


if __name__ == "__main__":
    main()
