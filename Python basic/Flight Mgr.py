"""
LTU Airport Flight Manager
D0043E – CodeGrade/Exam compliant solution

- No external libraries
- No built-in sorting (sorted(), .sort())
- Flights stored in a dictionary of dictionaries
- Bubble sort implemented manually and used for all sorting
- Program does not crash under normal use (handles invalid inputs with messages)
"""

VALID_STATUSES = ["Scheduled", "Boarding", "Departed"]


def bubble_sort(flight_list):
    """
    Sorts a list of flight numbers (strings) in ascending order using bubble sort.
    Returns the sorted list.
    """
    n = len(flight_list)
    i = 0
    while i < n - 1:
        j = 0
        while j < n - 1 - i:
            if flight_list[j] > flight_list[j + 1]:
                # Swap adjacent elements if out of order
                flight_list[j], flight_list[j + 1] = flight_list[j + 1], flight_list[j]
            j += 1
        i += 1
    return flight_list


def print_menu():
    """Print the main menu (must match the required text)."""
    print("# LTU Airport Flight Manager")
    print("1. Register a new flight")
    print("2. Update flight status")
    print("3. Remove a flight")
    print("4. View all flights")
    print("5. Find flights by status")
    print("6. Count total flights")
    print("q. Exit program")
    print("Enter your option:", end=" ")


def add_flight(flights):
    """
    Menu option 1:
    Add a new flight with validation rules and exact messages.
    """
    flight_no = input("Enter flight number: ").strip().upper()

    if len(flight_no) < 3:
        print("Error: Flight number must be at least 3 characters long.")
        return

    if flight_no in flights:
        print("Error: Flight number already exists.")
        return

    destination = input("Enter destination: ").strip()
    if destination == "":
        print("Error: Destination cannot be empty.")
        return

    status = input("Enter status (Scheduled/Boarding/Departed): ").strip()
    if status not in VALID_STATUSES:
        print("Error: Invalid status! Choose Scheduled, Boarding, or Departed.")
        return

    # Required dictionary-of-dictionaries structure
    flights[flight_no] = {"destination": destination, "status": status}
    print(f"Flight {flight_no} to {destination} added successfully!")


def update_status(flights):
    """
    Menu option 2:
    Update status of an existing flight, allow Enter to keep current status.
    """
    flight_no = input("Enter flight number: ").strip().upper()

    if flight_no not in flights:
        print("Error: Flight not found.")
        return

    current_status = flights[flight_no]["status"]
    print(f"Current status: {current_status}")

    new_status = input(
        "Enter new status (Scheduled/Boarding/Departed) or press Enter to keep the current status: "
    ).strip()

    # Pressing Enter keeps old status
    if new_status == "":
        print(f"Flight {flight_no} status updated successfully!")
        return

    if new_status not in VALID_STATUSES:
        print("Error: Invalid status! Choose Scheduled, Boarding, or Departed.")
        return

    flights[flight_no]["status"] = new_status
    print(f"Flight {flight_no} status updated successfully!")


def remove_flight(flights):
    """
    Menu option 3:
    Remove an existing flight by flight number.
    """
    flight_no = input("Enter flight number to remove: ").strip().upper()

    if flight_no not in flights:
        print("Error: Flight not found.")
        return

    del flights[flight_no]
    print(f"Flight {flight_no} removed successfully!")


def view_flights(flights):
    """
    Menu option 4:
    View all flights in ascending order by flight number using bubble sort.
    Prints a readable table with required headings/labels.
    """
    if len(flights) == 0:
        print("No flights registered.")
        return

    # Collect keys and sort with bubble sort (required)
    flight_numbers = list(flights.keys())
    flight_numbers = bubble_sort(flight_numbers)

    print("Current Flights:")
    print("-----------------------------------------------")
    print("Flight   Destination        Status")
    print("-----------------------------------------------")

    i = 0
    while i < len(flight_numbers):
        fn = flight_numbers[i]
        dest = flights[fn]["destination"]
        status = flights[fn]["status"]
        # Readable spacing (minor column width differences allowed)
        print(f"{fn:<8} {dest:<18} {status}")
        i += 1

    print("-----------------------------------------------")


def find_by_status(flights):
    """
    Menu option 5:
    Ask for a status, validate it, then list matching flights sorted by flight number.
    """
    status = input("Enter status to search for (Scheduled/Boarding/Departed): ").strip()

    if status not in VALID_STATUSES:
        print("Error: Invalid status! Choose Scheduled, Boarding, or Departed.")
        return

    # Collect matching flight numbers
    matches = []
    for fn in flights:
        if flights[fn]["status"] == status:
            matches.append(fn)

    if len(matches) == 0:
        print(f"No flights found with status {status}.")
        return

    matches = bubble_sort(matches)

    print(f"Flights with status {status}:")
    print("---------------------------------------")
    print("Flight   Destination")
    print("---------------------------------------")

    i = 0
    while i < len(matches):
        fn = matches[i]
        print(f"{fn:<8} {flights[fn]['destination']}")
        i += 1

    print("---------------------------------------")


def count_flights(flights):
    """
    Menu option 6:
    Print total number of flights in the required format.
    """
    print(f"Total flights registered: {len(flights)}")


def main():
    """
    Main loop:
    - prints menu
    - reads choice
    - calls correct function
    - exits only on 'q'
    """
    flights = {}

    while True:
        print_menu()
        choice = input().strip().lower()

        if choice == "1":
            add_flight(flights)
        elif choice == "2":
            update_status(flights)
        elif choice == "3":
            remove_flight(flights)
        elif choice == "4":
            view_flights(flights)
        elif choice == "5":
            find_by_status(flights)
        elif choice == "6":
            count_flights(flights)
        elif choice == "q":
            print("Goodbye!")
            break
        else:
            print("Invalid option! Please choose 1-6 or q.")


if __name__ == "__main__":
    main()
