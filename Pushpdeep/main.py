from parser import parse_tm_file


def main():
    file_path = "examples/valid.tm"

    try:
        tm = parse_tm_file(file_path)

        print("TM loaded successfully.")
        print("States:", tm.states)
        print("Input alphabet:", tm.input_alphabet)
        print("Tape alphabet:", tm.tape_alphabet)
        print("Blank symbol:", tm.blank)
        print("Start state:", tm.start_state)
        print("Accept state:", tm.accept_state)
        print("Reject state:", tm.reject_state)

        print("\nTransitions:")
        for key, action in tm.transitions.items():
            print(f"{key} -> ({action.next_state}, {action.write_symbol}, {action.direction})")

    except ValueError as e:
        print("Error while parsing TM:")
        print(e)


if __name__ == "__main__":
    main()