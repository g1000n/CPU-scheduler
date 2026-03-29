# Midterm Group Assignment 2: CPU Algorithms Simulation
# CS 301
# Group Members:
# - Ashley Buenafe Dyriel
# - Rendel Gion B. Lobo
# - Alexia John Pamintuan
# - Anoucshka Ysabeli A. Sison



# input function
def get_process_input(with_priority=False):
    count = int(input("Enter number of processes: "))
    processes = []

    for i in range(count):
        print(f"\nProcess P{i+1}")
        arrival = int(input("Arrival Time: "))
        burst = int(input("Burst Time: "))

        process = {
            "pid": f"P{i+1}",
            "arrival": arrival,
            "burst": burst,
            "remaining": burst
        }

        if with_priority:
            priority = int(input("Priority (lower number = higher priority): "))
            process["priority"] = priority

        processes.append(process)

    return processes


# displaying results
def show_results(processes):
    total_wt = 0
    total_tt = 0

    print("\nPID\tWaiting\tTurnaround")

    for p in processes:
        print(f"{p['pid']}\t{p['waiting']}\t{p['turnaround']}")
        total_wt += p["waiting"]
        total_tt += p["turnaround"]

    avg_wt = total_wt / len(processes)
    avg_tt = total_tt / len(processes)

    # format to 2 decimal places
    print(f"\nAverage Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tt:.2f}")



# FCFS
def fcfs():
    print("\n--- FCFS Scheduling ---")

    processes = get_process_input()

    # sort by arrival time
    processes.sort(key=lambda x: x["arrival"])

    current_time = 0

    for p in processes:
        if current_time < p["arrival"]:
            current_time = p["arrival"]

        start_time = current_time
        finish_time = start_time + p["burst"]

        p["waiting"] = start_time - p["arrival"]
        p["turnaround"] = finish_time - p["arrival"]

        current_time = finish_time

    show_results(processes)


# SRTF
def srtf():
    print("\n--- SRTF Scheduling ---")

    processes = get_process_input()

    time = 0
    completed = 0
    total = len(processes)

    while completed < total:

        # get processes that arrived and still have remaining time
        ready = [p for p in processes if p["arrival"] <= time and p["remaining"] > 0]

        if not ready:
            time += 1
            continue

        # choose process with smallest remaining time
        current = min(ready, key=lambda x: x["remaining"])

        current["remaining"] -= 1
        time += 1

        if current["remaining"] == 0:
            completed += 1
            completion_time = time
            current["turnaround"] = completion_time - current["arrival"]
            current["waiting"] = current["turnaround"] - current["burst"]

    show_results(processes)


# ROUND ROBIN
def round_robin():
    print("\n--- Round Robin Scheduling ---")

    processes = get_process_input()
    quantum = int(input("Enter Time Quantum: "))

    processes.sort(key=lambda x: x["arrival"])

    time = 0
    queue = []
    index = 0
    completed = 0
    total = len(processes)

    while completed < total:

        # add newly arrived processes to queue
        while index < total and processes[index]["arrival"] <= time:
            queue.append(processes[index])
            index += 1

        if not queue:
            time += 1
            continue

        current = queue.pop(0)

        execution_time = min(current["remaining"], quantum)

        time += execution_time
        current["remaining"] -= execution_time

        # add new arrivals during execution
        while index < total and processes[index]["arrival"] <= time:
            queue.append(processes[index])
            index += 1

        if current["remaining"] == 0:
            completed += 1
            completion_time = time
            current["turnaround"] = completion_time - current["arrival"]
            current["waiting"] = current["turnaround"] - current["burst"]
        else:
            queue.append(current)

    show_results(processes)


# NON-PREEMPTIVE PRIORITY
def non_preemptive_priority():
    print("\n--- Non-Preemptive Priority Scheduling ---")

    processes = get_process_input(with_priority=True)

    time = 0
    completed = 0
    total = len(processes)

    while completed < total:

        # select available processes
        ready = [p for p in processes if p["arrival"] <= time and p["remaining"] > 0]

        if not ready:
            time += 1
            continue

        # lower number = higher priority
        current = min(ready, key=lambda x: x["priority"])

        start_time = time
        finish_time = start_time + current["burst"]

        current["remaining"] = 0
        completed += 1

        current["turnaround"] = finish_time - current["arrival"]
        current["waiting"] = current["turnaround"] - current["burst"]

        time = finish_time

    show_results(processes)


# main menu
def main():
    while True:
        print("\nCPU Scheduling Simulator")
        print("1 - FCFS")
        print("2 - SRTF")
        print("3 - Round Robin")
        print("4 - Non-Preemptive Priority")
        print("5 - Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            fcfs()
        elif choice == "2":
            srtf()
        elif choice == "3":
            round_robin()
        elif choice == "4":
            non_preemptive_priority()
        elif choice == "5":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
