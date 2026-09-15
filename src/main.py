import sys
import pandas as pd
from src.database import init_db, add_expense, get_all_expenses

def display_menu():
    """Displays the main menu options to the user."""
    print("\n" + "="*40)
    print("💰 PERSONAL EXPENSE TRACKER 💰")
    print("="*40)
    print("1. Add an Expense")
    print("2. View All Expenses & Summary")
    print("3. Exit")
    print("="*40)

def handle_add_expense():
    """Handles the user input for adding a new expense."""
    print("\n--- Add New Expense ---")
    
    # Input validation for Amount
    while True:
        try:
            amount = float(input("Enter amount ($): "))
            if amount <= 0:
                print("❌ Amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")
            
    category = input("Enter category (e.g., Food, Transport, Bills): ").strip().capitalize()
    description = input("Enter description (optional): ").strip()
    
    # Call the database function we wrote earlier
    add_expense(amount, category, description)
    input("\nPress Enter to return to the main menu...")

def handle_view_expenses():
    """Fetches data, converts to a Pandas DataFrame, and displays a summary."""
    print("\n--- Your Expenses ---")
    
    expenses = get_all_expenses()
    
    if not expenses:
        print("No expenses recorded yet. Start adding some!")
        input("\nPress Enter to return to the main menu...")
        return

    # Convert the list of tuples into a Pandas DataFrame
    df = pd.DataFrame(expenses, columns=["ID", "Date", "Amount", "Category", "Description"])
    
    # Print the DataFrame without the index column
    print(df.to_string(index=False))
    
    # Calculate total spent using Pandas
    total_spent = df["Amount"].sum()
    print("-" * 40)
    print(f"💵 TOTAL SPENT: ${total_spent:.2f}")
    print("-" * 40)
    
    # Optional: Show spending by category
    print("\n📊 Spending by Category:")
    category_summary = df.groupby("Category")["Amount"].sum().reset_index()
    for index, row in category_summary.iterrows():
        print(f"  - {row['Category']}: ${row['Amount']:.2f}")

    input("\nPress Enter to return to the main menu...")

def main():
    """The main entry point of the application."""
    # Initialize the database (creates the table if it doesn't exist)
    init_db()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            handle_add_expense()
        elif choice == "2":
            handle_view_expenses()
        elif choice == "3":
            print("\n👋 Thank you for using the Expense Tracker. Goodbye!")
            sys.exit()
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()