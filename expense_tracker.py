import csv
from datetime import datetime
import os

FILE_NAME = "expenses.csv"
HEADERS = ["Date", "Category", "Amount", "Description"]


def initialize_file():
    """Create CSV file with headers if it does not already exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)


def add_expense():
    """Prompt user and append a new expense row."""
    date_input = input(
        "Enter date (YYYY-MM-DD) or press Enter for today: "
    ).strip()
    if not date_input:
        date_input = datetime.today().strftime("%Y-%m-%d")
    else:
        # Validate date format
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Using today's date instead.")
            date_input = datetime.today().strftime("%Y-%m-%d")

    category = (
        input("Enter category (Food, Transport, Rent, Bills, Other): ")
        .strip()
        .capitalize()
    )

    while True:
        try:
            amount = float(input("Enter amount: ").strip())
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            break
        except ValueError:
            print("Invalid number. Please enter a valid decimal or integer.")

    description = input("Enter brief description: ").strip()

    with open(FILE_NAME, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date_input, category, f"{amount:.2f}", description])

    print("\n✓ Expense recorded successfully!\n")


def view_expenses():
    """Read and format all expenses in a clean table."""
    if not os.path.exists(FILE_NAME):
        print("\nNo expenses recorded yet.\n")
        return

    with open(FILE_NAME, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)

    if len(rows) <= 1:
        print("\nNo expenses found.\n")
        return

    print("\n" + "=" * 60)
    print(f"{'Date':<12} | {'Category':<15} | {'Amount ($)':<10} | {'Description'}")
    print("-" * 60)

    total = 0.0
    for row in rows[1:]:
        date, category, amount, desc = row
        total += float(amount)
        print(f"{date:<12} | {category:<15} | {amount:<10} | {desc}")

    print("-" * 60)
    print(f"Total Spent: ${total:.2f}")
    print("=" * 60 + "\n")


def category_summary():
    """Group spending totals by category."""
    if not os.path.exists(FILE_NAME):
        print("\nNo expenses recorded yet.\n")
        return

    with open(FILE_NAME, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)

    if len(rows) <= 1:
        print("\nNo expenses found.\n")
        return

    totals = {}
    for row in rows[1:]:
        category = row[1]
        amount = float(row[2])
        totals[category] = totals.get(category, 0.0) + amount

    print("\n" + "=" * 35)
    print(f"{'Category':<20} | {'Total ($)'}")
    print("-" * 35)
    for cat, amt in totals.items():
        print(f"{cat:<20} | ${amt:.2f}")
    print("=" * 35 + "\n")


def main():
    initialize_file()
    while True:
        print("--- Simple Expense Tracker ---")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Category Summary")
        print("4. Exit")

        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            category_summary()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid selection. Please choose between 1 and 4.\n")


if __name__ == "__main__":
    main()