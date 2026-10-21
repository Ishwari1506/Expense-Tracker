# CLI Expense Tracker

This is a simple Python application to manage daily expenses through a command-line interface.

## Features
- Add an expense with description, amount, and category.
- View all expenses.
- Filter expenses by category.
- Delete an expense using its ID.
- Save expenses in a JSON file.

## Requirements
- Python 3.6 or newer

## How to Run

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Run the following command:

   ```bash
   python main.py
   ```

## Data Storage
Expenses are stored locally in expenses.json. The file is created automatically when an expense is saved.

## Usage
===== CLI Expense Tracker =====
1. Add Expense
2. View Expenses
3. Delete Expense
4. Exit

```text
Enter your choice (1-4): 1
Enter description: Lunch
Enter amount: 150
Enter category: Food

Expense added successfully. ID: 1

Enter your choice (1-4): 2
Enter category to filter, or press Enter to view all:Food

-----------------------------------------------------------------
ID    Description           Amount         Category
-----------------------------------------------------------------
1     Lunch                 150.00         Food
-----------------------------------------------------------------
Total: 150.00

Enter your choice (1-4): 3
Enter the ID of the expense to delete: 1

Expense 'Lunch' deleted successfully.
```
