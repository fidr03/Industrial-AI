"""
LTU Rent-a-Car
Author: Filip Drincic 030909-4973, LTU
- Python program for a simple Car Rental System for a small company.
- The program allows the user to register cars for rent, rent and return cars, view all registered cars, and search for rental summary.
- A dictionary used to store the fleet of cars
- Bubble sort implemented manually and used for sorting
"""

# ===============================
# Global data storage
# ===============================
cars = {}
rentals = []


# ===============================
# Bubble sort
# ===============================
def bubble_sort(items):
    """Sorts a list in ascending order using bubble sort."""
    n = len(items)
    for i in range(n):
        for j in range(0, n - i - 1):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]


# ===============================
# Menu
# ===============================
def print_menu():
    """Prints the main menu options."""
    print("# LTU Rent-a-Car")
    print("1. Add car to fleet")
    print("2. Rent a car")
    print("3. Return a car")
    print("4. View car fleet")
    print("5. View rental summary")
    print("q. Exit program")


# ===============================
# Menu option 1 – Add car to fleet
# ===============================
def add_car():
    """Adds a new car to the car fleet after validation."""
    reg = input("Enter registration number: ")
    if len(reg) < 4:
        print("Error: Registration number must be at least 4 characters long.")
        return
    if " " in reg:
        print("Error: Registration number cannot contain spaces.")
        return
    if reg in cars:
        print("Error: Registration number already exists.")
        return

    model = input("Enter make and model: ")
    if model.strip() == "":
        print("Error: Make and model cannot be empty.")
        return

    cars[reg] = {
        "model": model,
        "status": "Available"
    }

    print(f"{model} with registration number {reg} was added to car fleet.")


# ===============================
# Menu option 2 – Rent a car
# ===============================
def rent_car():
    """Rents an available car to a customer."""
    reg = input("Enter car's registration number: ")

    if len(reg) < 4:
        print("Error: Registration number must be at least 4 characters long.")
        return
    if " " in reg:
        print("Error: Registration number cannot contain spaces.")
        return
    if reg not in cars:
        print("Error: Car not found.")
        return
    if cars[reg]["status"] != "Available":
        print("Error: Car is not available.")
        return

    hour_input = input("Enter pickup hour (0-23): ")
    if not hour_input.isdigit():
        print("Error: Invalid hour! Please enter an integer between 0 and 23.")
        return

    start_hour = int(hour_input)
    if start_hour < 0 or start_hour > 23:
        print("Error: Invalid hour! Please enter an integer between 0 and 23.")
        return

    renter = input("Enter renter's name: ")
    if renter.strip() == "":
        print("Error: Renter name cannot be empty.")
        return

    cars[reg]["status"] = "Rented"

    rentals.append({
        "reg": reg,
        "renter": renter,
        "start_hour": start_hour,
        "end_hour": None,
        "hours": None,
        "cost": None
    })

    print(f"Car with registration number {reg} was rented by {renter} at {start_hour}.")


# ===============================
# Menu option 3 – Return a car
# ===============================
def return_car():
    """Processes the return of a rented car and prints a receipt."""
    reg = input("Enter registration number: ")

    if len(reg) < 4:
        print("Error: Registration number must be at least 4 characters long.")
        return
    if " " in reg:
        print("Error: Registration number cannot contain spaces.")
        return
    if reg not in cars:
        print("Error: Car not found.")
        return
    if cars[reg]["status"] != "Rented":
        print("Error: Car is not rented.")
        return

    hour_input = input("Enter return hour (0-23): ")
    if not hour_input.isdigit():
        print("Error: Invalid hour! Please enter an integer between 0 and 23.")
        return

    end_hour = int(hour_input)
    if end_hour < 0 or end_hour > 23:
        print("Error: Invalid hour! Please enter an integer between 0 and 23.")
        return

    active_rental = None
    for rental in rentals:
        if rental["reg"] == reg and rental["end_hour"] is None:
            active_rental = rental
            break

    start_hour = active_rental["start_hour"]
    if end_hour <= start_hour:
        print("Error: Return hour must be later than pickup hour.")
        return

    hours = end_hour - start_hour
    cost = hours * 120

    active_rental["end_hour"] = end_hour
    active_rental["hours"] = hours
    active_rental["cost"] = cost
    cars[reg]["status"] = "Available"

    print("===================================")
    print("LTU Rent-a-Car")
    print("===================================")
    print(f"Name: {active_rental['renter']}")
    print(f"Car: {cars[reg]['model']} ({reg})")
    print(f"Time: {start_hour}-{end_hour} ({hours} hours)")
    print(f"Total cost: {cost} SEK")


# ===============================
# Menu option 4 – View car fleet
# ===============================
def view_fleet():
    """Displays all cars in the fleet in sorted order."""
    if not cars:
        print("No cars in fleet.")
        return

    reg_numbers = list(cars.keys())
    bubble_sort(reg_numbers)

    print("LTU Rent-a-Car car fleet:")
    print("Fleet:")
    print(f"{'Model':20} {'Registration':14} Status")

    available = 0
    for reg in reg_numbers:
        model = cars[reg]["model"]
        status = cars[reg]["status"]
        if status == "Available":
            available += 1
        print(f"{model:20} {reg:14} {status}")

    print(f"Total number of cars: {len(cars)}")
    print(f"Total number of available cars: {available}")


# ===============================
# Menu option 5 – View rental summary
# ===============================
def view_rentals():
    """Displays a summary of all rentals sorted by renter name."""
    if not rentals:
        print("No rentals for today.")
        return

    names = []
    for rental in rentals:
        names.append(rental["renter"])

    bubble_sort(names)

    print("LTU Rent-a-Car rental summary:")
    print("Rentals:")
    print(f"{'Name':18} {'Registration':13} Pickup  Return  Cost")

    printed = set()
    total_revenue = 0

    for name in names:
        for rental in rentals:
            if rental["renter"] == name and id(rental) not in printed:
                printed.add(id(rental))

                reg = rental["reg"]
                pickup = rental["start_hour"]
                ret = "" if rental["end_hour"] is None else rental["end_hour"]
                cost = "" if rental["cost"] is None else f"{rental['cost']} SEK"

                if rental["cost"] is not None:
                    total_revenue += rental["cost"]

                print(f"{name:18} {reg:13} {pickup:<7} {ret:<7} {cost}")
                break

    print(f"Total number of rentals: {len(rentals)}")
    print(f"Total revenue: {total_revenue} SEK")


# ===============================
# Main loop
# ===============================
def main():
    """Main program loop handling menu navigation."""
    while True:
        print_menu()
        option = input("Enter your option: ")

        if option == "1":
            add_car()
        elif option == "2":
            rent_car()
        elif option == "3":
            return_car()
        elif option == "4":
            view_fleet()
        elif option == "5":
            view_rentals()
        elif option == "q":
            print("Goodbye!")
            break
        else:
            print("Invalid option! Please choose 1-5 or q.")

        print()


# ===============================
# Program entry point
# ===============================
if __name__ == "__main__":
    main()
