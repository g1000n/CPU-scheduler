# =========================================================
# PAGED REPLACEMENT SIMULATION PROJECT
# Group Members:
# - Ashley Dyriel V. Buenafe
# - Rendel Gion B. Lobo
# - Alexia John D. Pamintuan
# - Anoucshka Ysabeli A. Sison
#
# Required Algorithms:
# 1. FIFO
# 2. LRU
# 3. MRU
# 4. OPTIMAL
# 5. SECOND CHANCE
#
# Notes:
# - This program is an original implementation.
# - External materials may be used only as references for understanding.
# - Cite all sources properly in the report.
# =========================================================


# ---------------------------
# Utility Functions
# ---------------------------

def parse_reference_string(ref_input):
    """
    Converts a space-separated reference string into a list of integers.
    Example: "7 0 1 2 0 3" -> [7, 0, 1, 2, 0, 3]
    """
    return [int(x) for x in ref_input.strip().split()]


def calculate_rates(total_references, page_faults):
    """
    Returns page hits, failure rate, and success rate.
    """
    page_hits = total_references - page_faults
    failure_rate = (page_faults / total_references) * 100 if total_references > 0 else 0
    success_rate = (page_hits / total_references) * 100 if total_references > 0 else 0
    return page_hits, failure_rate, success_rate


def format_frames(frames, num_frames):
    """
    Pads frame contents with '-' so the output table remains aligned.
    """
    return frames[:] + ["-"] * (num_frames - len(frames))


def record_step(steps, step_number, page, frames, num_frames, interrupt, note=""):
    """
    Saves one simulation step for later display.
    """
    steps.append({
        "step": step_number,
        "page": page,
        "frames": format_frames(frames, num_frames),
        "interrupt": interrupt,
        "note": note
    })


def print_results(algorithm_name, reference_string, num_frames, steps, page_faults):
    """
    Displays the complete simulation table and summary.
    """
    total_pages = len(reference_string)
    page_hits, failure_rate, success_rate = calculate_rates(total_pages, page_faults)

    print("\n" + "=" * 120)
    print(f"Algorithm: {algorithm_name}")
    print(f"Number of Pages: {total_pages}")
    print(f"Number of Frames: {num_frames}")
    print("Page Reference String:", " ".join(map(str, reference_string)))
    print("=" * 120)

    # Table Header
    header = ["Step", "Page"] + [f"Frame{i+1}" for i in range(num_frames)] + ["Interrupt", "Result / Notes"]
    print(f"{header[0]:<8}{header[1]:<8}", end="")
    for i in range(num_frames):
        print(f"{header[i+2]:<10}", end="")
    print(f"{header[-2]:<12}{header[-1]:<25}")

    print("-" * 120)

    # Table Rows
    for step in steps:
        print(f"{step['step']:<8}{step['page']:<8}", end="")
        for frame_value in step["frames"]:
            print(f"{str(frame_value):<10}", end="")
        print(f"{step['interrupt']:<12}{step['note']:<25}")

    print("-" * 120)
    print(f"Total Page Faults (Failures): {page_faults}")
    print(f"Total Page Hits (Successes): {page_hits}")
    print(f"Failure Rate: {failure_rate:.2f}%")
    print(f"Success Rate: {success_rate:.2f}%")
    print("=" * 120)


# ---------------------------
# FIFO
# ---------------------------

def fifo(reference_string, num_frames):
    frames = []
    pointer = 0
    page_faults = 0
    steps = []

    for step_number, page in enumerate(reference_string, start=1):
        if page in frames:
            record_step(steps, step_number, page, frames, num_frames, "No", "Hit")
        else:
            page_faults += 1

            if len(frames) < num_frames:
                frames.append(page)
            else:
                frames[pointer] = page
                pointer = (pointer + 1) % num_frames

            record_step(steps, step_number, page, frames, num_frames, "Yes", "Fault")

    return steps, page_faults


# ---------------------------
# LRU
# ---------------------------

def lru(reference_string, num_frames):
    frames = []
    last_used = {}
    page_faults = 0
    steps = []

    for step_number, page in enumerate(reference_string, start=1):
        if page in frames:
            last_used[page] = step_number
            record_step(steps, step_number, page, frames, num_frames, "No", "Hit")
        else:
            page_faults += 1

            if len(frames) < num_frames:
                frames.append(page)
            else:
                victim = min(frames, key=lambda p: last_used[p])
                victim_index = frames.index(victim)
                frames[victim_index] = page

            last_used[page] = step_number
            record_step(steps, step_number, page, frames, num_frames, "Yes", "Fault")

    return steps, page_faults


# ---------------------------
# MRU
# ---------------------------

def mru(reference_string, num_frames):
    frames = []
    last_used = {}
    page_faults = 0
    steps = []

    for step_number, page in enumerate(reference_string, start=1):
        if page in frames:
            last_used[page] = step_number
            record_step(steps, step_number, page, frames, num_frames, "No", "Hit")
        else:
            page_faults += 1

            if len(frames) < num_frames:
                frames.append(page)
            else:
                victim = max(frames, key=lambda p: last_used[p])
                victim_index = frames.index(victim)
                frames[victim_index] = page

            last_used[page] = step_number
            record_step(steps, step_number, page, frames, num_frames, "Yes", "Fault")

    return steps, page_faults


# ---------------------------
# OPTIMAL
# ---------------------------

def optimal(reference_string, num_frames):
    frames = []
    page_faults = 0
    steps = []

    for current_index, page in enumerate(reference_string):
        step_number = current_index + 1

        if page in frames:
            record_step(steps, step_number, page, frames, num_frames, "No", "Hit")
        else:
            page_faults += 1

            if len(frames) < num_frames:
                frames.append(page)
            else:
                future_use = {}

                for frame_page in frames:
                    if frame_page in reference_string[current_index + 1:]:
                        next_index = reference_string[current_index + 1:].index(frame_page)
                        future_use[frame_page] = next_index
                    else:
                        future_use[frame_page] = float("inf")

                victim = max(future_use, key=future_use.get)
                victim_index = frames.index(victim)
                frames[victim_index] = page

            record_step(steps, step_number, page, frames, num_frames, "Yes", "Fault")

    return steps, page_faults


# ---------------------------
# SECOND CHANCE
# ---------------------------

def second_chance(reference_string, num_frames):
    frames = []
    reference_bits = []
    pointer = 0
    page_faults = 0
    steps = []

    for step_number, page in enumerate(reference_string, start=1):
        if page in frames:
            page_index = frames.index(page)
            reference_bits[page_index] = 1

            bits_display = reference_bits[:] + ["-"] * (num_frames - len(reference_bits))
            note = "Hit | Bits: " + " ".join(map(str, bits_display))
            record_step(steps, step_number, page, frames, num_frames, "No", note)

        else:
            page_faults += 1

            if len(frames) < num_frames:
                frames.append(page)
                reference_bits.append(1)
            else:
                while True:
                    if reference_bits[pointer] == 0:
                        frames[pointer] = page
                        reference_bits[pointer] = 1
                        pointer = (pointer + 1) % num_frames
                        break
                    else:
                        reference_bits[pointer] = 0
                        pointer = (pointer + 1) % num_frames

            bits_display = reference_bits[:] + ["-"] * (num_frames - len(reference_bits))
            note = "Fault | Bits: " + " ".join(map(str, bits_display))
            record_step(steps, step_number, page, frames, num_frames, "Yes", note)

    return steps, page_faults


# ---------------------------
# Input / Menu Functions
# ---------------------------

def get_user_input():
    """
    Gets validated user input for number of frames and reference string.
    """
    while True:
        try:
            num_frames = int(input("Enter number of frames: "))
            if num_frames <= 0:
                print("Number of frames must be greater than 0.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    while True:
        try:
            ref_input = input("Enter page reference string (space-separated integers): ")
            reference_string = parse_reference_string(ref_input)
            if len(reference_string) == 0:
                print("Reference string cannot be empty.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter integers only, separated by spaces.")

    return num_frames, reference_string


def display_menu():
    print("\n" + "=" * 60)
    print("PAGED REPLACEMENT SIMULATION")
    print("=" * 60)
    print("1. FIFO")
    print("2. LRU")
    print("3. MRU")
    print("4. OPTIMAL")
    print("5. SECOND CHANCE")
    print("6. Run All Algorithms")
    print("7. Run Predefined Test Cases")
    print("8. Exit")
    print("=" * 60)


def run_single_algorithm(choice, num_frames, reference_string):
    if choice == "1":
        steps, faults = fifo(reference_string, num_frames)
        print_results("FIFO", reference_string, num_frames, steps, faults)

    elif choice == "2":
        steps, faults = lru(reference_string, num_frames)
        print_results("LRU", reference_string, num_frames, steps, faults)

    elif choice == "3":
        steps, faults = mru(reference_string, num_frames)
        print_results("MRU", reference_string, num_frames, steps, faults)

    elif choice == "4":
        steps, faults = optimal(reference_string, num_frames)
        print_results("OPTIMAL", reference_string, num_frames, steps, faults)

    elif choice == "5":
        steps, faults = second_chance(reference_string, num_frames)
        print_results("SECOND CHANCE", reference_string, num_frames, steps, faults)


def run_all_algorithms(num_frames, reference_string):
    algorithms = [
        ("FIFO", fifo),
        ("LRU", lru),
        ("MRU", mru),
        ("OPTIMAL", optimal),
        ("SECOND CHANCE", second_chance)
    ]

    for name, function in algorithms:
        steps, faults = function(reference_string, num_frames)
        print_results(name, reference_string, num_frames, steps, faults)


def run_predefined_test_cases():
    """
    Useful for screenshots and sample outputs in the report.
    """
    test_cases = [
        {
            "label": "Test Case 1",
            "frames": 3,
            "reference": [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
        },
        {
            "label": "Test Case 2",
            "frames": 4,
            "reference": [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
        },
        {
            "label": "Test Case 3",
            "frames": 3,
            "reference": [0, 4, 1, 4, 2, 4, 3, 4, 2, 4, 0, 4, 1, 4, 2, 4, 3, 4]
        }
    ]

    for case in test_cases:
        print("\n" + "#" * 120)
        print(case["label"])
        print("#" * 120)
        run_all_algorithms(case["frames"], case["reference"])


# ---------------------------
# Main Program
# ---------------------------

def main():
    while True:
        display_menu()
        choice = input("Choose an option (1-8): ").strip()

        if choice == "8":
            print("Exiting program...")
            break

        if choice == "7":
            run_predefined_test_cases()
            continue

        if choice not in ["1", "2", "3", "4", "5", "6"]:
            print("Invalid choice. Please choose from 1 to 8.")
            continue

        num_frames, reference_string = get_user_input()

        if choice == "6":
            run_all_algorithms(num_frames, reference_string)
        else:
            run_single_algorithm(choice, num_frames, reference_string)


if __name__ == "__main__":
    main()