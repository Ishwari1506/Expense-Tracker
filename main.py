import json
from pathlib import Path
import math
from datetime import date


FILE_PATH = Path(__file__).parent / "expenses.json"


class Expense:
    """Represents a single expense."""

    def __init__(self, expense_id, description, amount, category,
                 expense_date=None):
        self.id = expense_id
        self.description = description
        self.amount = amount
        self.category = category
        self.date = expense_date or date.today().isoformat()

    def to_dict(self):
        """Convert the expense object into a dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "amount": self.amount,
            "category": self.category,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Expense object from a dictionary."""
        return cls(
            data["id"],
            data["description"],
            data["amount"],
            data["category"],
            data.get("date")
        )


def load_expenses():
    """Load expenses from the JSON file."""
    if not FILE_PATH.exists():
        return []

    try:
        with FILE_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("The JSON file must contain a list.")

        return [Expense.from_dict(item) for item in data]

    except (json.JSONDecodeError, ValueError, KeyError, TypeError) as error:
        print(f"Could not load expenses: {error}")
        print("Please check expenses.json. Existing data has not been overwritten.")
        return None

    except OSError as error:
        print(f"Could not read expenses.json: {error}")
        return None


def save_expenses(expenses):
    """Save all expenses to the JSON file."""
    try:
        with FILE_PATH.open("w", encoding="utf-8") as file:
            json.dump(
                [expense.to_dict() for expense in expenses],
                file,
                indent=4
            )
        return True

    except OSError as error:
        print(f"Could not save expenses: {error}")
        return False


def add_expense(expenses):
    """Ask for expense details and add a new expense."""
    description = input("Enter description: ").strip()

    if not description:
        print("Description cannot be empty.")
        return

    try:
        amount = float(input("Enter amount: "))

        if not math.isfinite(amount) or amount <= 0:
            print("Amount must be a positive, finite number.")
            return

    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    category = input("Enter category: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    # Generate a unique ID based on existing expenses.
    expense_id = max((expense.id for expense in expenses), default=0) + 1

    expense = Expense(expense_id, description, amount, category)
    expenses.append(expense)

    if save_expenses(expenses):
        print(f"Expense added successfully. ID: {expense_id}")
    else:
        expenses.pop()
        print("Expense was not added because it could not be saved.")


def view_expenses(expenses):
    """Display all expenses or filter by category."""
    if not expenses:
        print("No expenses found.")
        return

    category = input(
        "Enter category to filter, or press Enter to view all: "
    ).strip()

    if category:
        filtered_expenses = [
            expense for expense in expenses
            if expense.category.casefold() == category.casefold()
        ]
    else:
        filtered_expenses = expenses

    if not filtered_expenses:
        print(f"No expenses found in category '{category}'.")
        return

    print("\n" + "-" * 65)
    print(f"{'ID':<6}{'Description':<22}{'Amount':<15}{'Category':<20}")
    print("-" * 65)

    total = 0

    for expense in filtered_expenses:
        print(
            f"{expense.id:<6}"
            f"{expense.description[:20]:<22}"
            f"{expense.amount:<15.2f}"
            f"{expense.category[:18]:<20}"
        )
        total += expense.amount

    print("-" * 65)
    print(f"Total: {total:.2f}")
    print()


def delete_expense(expenses):
    """Delete an expense using its ID."""
    if not expenses:
        print("No expenses available to delete.")
        return

    try:
        expense_id = int(input("Enter the ID of the expense to delete: "))
    except ValueError:
        print("Invalid ID. Please enter a whole number.")
        return

    for index, expense in enumerate(expenses):
        if expense.id == expense_id:
            deleted_expense = expenses.pop(index)

            if save_expenses(expenses):
                print(
                    f"Expense '{deleted_expense.description}' "
                    "deleted successfully."
                )
            else:
                # Restore the expense if saving failed.
                expenses.insert(index, deleted_expense)
                print("Could not save changes. Expense was not deleted.")
            return

    print(f"No expense found with ID {expense_id}.")


def monthly_summary(expenses):
    """Display and export a monthly summary by category."""
    from datetime import datetime
    from collections import defaultdict

    month = input("Enter month (YYYY-MM, e.g., 2026-10): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format. Please use YYYY-MM.")
        return

    category_totals = defaultdict(float)

    for expense in expenses:
        try:
            expense_date = datetime.strptime(expense.date, "%Y-%m-%d")
        except (ValueError, TypeError):
            continue

        if expense_date.strftime("%Y-%m") == month:
            category_totals[expense.category.casefold()] += expense.amount

    if not category_totals:
        print(f"No expenses found for {month}.")
        return

    lines = [
        f"Monthly Expense Summary - {month}",
        "=" * 40
    ]

    for category, total in sorted(category_totals.items()):
        lines.append(f"{category.title():<20} {total:.2f}")

    grand_total = sum(category_totals.values())
    lines.extend([
        "-" * 40,
        f"{'Grand Total':<20} {grand_total:.2f}"
    ])

    summary_text = "\n".join(lines)

    print("\n" + summary_text)

    report_path = FILE_PATH.parent / f"monthly_summary_{month}.txt"

    try:
        report_path.write_text(summary_text + "\n", encoding="utf-8")
        print(f"\nSummary exported to: {report_path.name}")
    except OSError as error:
        print(f"Could not export summary: {error}")



def main():
    """Run the menu-driven expense tracker."""
    expenses = load_expenses()

    if expenses is None:
        print("Please fix the JSON file before running the application.")
        return

    while True:
        print("\n===== CLI Expense Tracker =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Monthly Summary")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            delete_expense(expenses)
        elif choice == "4":
            monthly_summary(expenses)
        elif choice == "5":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
