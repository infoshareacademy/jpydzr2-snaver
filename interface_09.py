
from models.Budget import Budget
from models.Category import Category
from models.ParentCategory import ParentCategory
from models.Transaction import Transaction
from models.User import User
from controllers.budget_controller import add_new_budget
from session import session

from prettytable import PrettyTable
from sqlalchemy import insert
import sqlite3
from prettytable import from_db_cursor

from sqlalchemy.orm import lazyload, joinedload

# global work_in_progress
# work_in_progress= "@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget."

def menu():
    print("MENU:")
    print("0. Change user")
    print("1. Change budget")
    print("2. New transaction (activity)")
    print("3. Edit categories")
    print("4. Edit budget (modify budgeted amounts)")
    print("5. Switch the month (the billing peroid")
    print("6. Reports")
    print("7. Save and close the program")
    choice = input("## YOUR CHOICE: ")

    if choice == "0":
        change_user()
    if choice == "1":
        change_budget()
    if choice == "2":
        new_transaction()
    if choice == "3":
        edit_categories()
    if choice == "4":
        edit_budget()
    if choice == "5":
        switch_month()
    if choice == "6":
        reports()
    if choice == "7":
        print("End. Program closed.")
        pass
    else:
        print("\n!!! >>> WRONG CHOICE (OUT OF RANGE). TRY AGAIN...")
        menu()


def change_user():
    global user_to_show
    user_to_show = input("\nInput user's id: ")
    print(f"\nUser >>id={user_to_show}<< logged in.")       # TODO: Here should be "User {user.name} logged in."
    change_budget()


def change_budget():
    print("\nYour budgetes:")

    ''' Printing the table with user's budgetes.'''
    # Definition of PrettyTable for budgetes.
    table_show_budgetes = PrettyTable()
    table_show_budgetes.field_names = ["id", "name"]

    # Reading data from databe and inserting into PrettyTable
    for instance in session.query(Budget).filter(Budget.user_id == user_to_show):
        table_show_budgetes.add_row([Budget.give_budgets(instance)[0], Budget.give_budgets(instance)[1]])

    print(table_show_budgetes)


    ''' Printing the budget's table that user selected.'''
    global budget_to_show
    # budget_to_show = input("Which budget to show? Input budget's id: ")
    budget_to_show = input("Which budget to show? Input budget's id OR input 'n' to create new budget: ")
    if budget_to_show == 'n':
        add_new_budget(user_to_show)
    print_budget()


def print_budget():

    # Definition of PrettyTable
    table_budget = PrettyTable()
    table_budget.field_names = [" id, CATEGORY", "BUDGETED", "ACTIVITY", "AVAILABLE"]
    table_budget.align = "r"   # align in all columns to the right side
    table_budget.align[" id, CATEGORY"] = "l"   # align in column "CATEGORY" to the left side
    table_budget.float_format = "1.2"  # the way floating point data is printed

    # Reading data from database and inserting into PrettyTable
    sum_budgeted = 0
    sum_available = 0
    total_budgeted = 0
    total_activity = 0
    total_available = 0


    for instance in session.query(ParentCategory).filter(ParentCategory.budget_id == budget_to_show):

        # adding up values from categories and assigning them to parent_categories
        for value_budgeted in session.query(Category).filter(Category.parent_id == ParentCategory.give_parent_categories(instance)[0]):
            sum_budgeted += (Category.give_info(value_budgeted)[1])

        for value_available in session.query(Category).filter(Category.parent_id == ParentCategory.give_parent_categories(instance)[0]):
            sum_available += (Category.give_info(value_available)[3])

        sum_activity = sum_budgeted - sum_available


        # Below code adds rows to PrettyTable like this:
        # | -------------------- | -------------------- | -------------------- | -------------------- |
        # | parent_category      |               xxx.xx |               yyy.yy |               zzz.zz |
        # | -------------------- | -------------------- | -------------------- | -------------------- |
        table_budget.add_row([30*"-", 10*"-", 10*"-", 10*"-"])
        table_budget.add_row([ParentCategory.give_parent_categories(instance), sum_budgeted, sum_activity, sum_available])
        table_budget.add_row([30*"-", 10*"-", 10*"-", 10*"-"])

        total_budgeted += sum_budgeted
        total_activity += sum_activity
        total_available += sum_available

        sum_budgeted = 0    # this is reset to zero to allow summing categories in next parent-categories
        sum_available = 0   # this is reset to zero to allow summing categories in next parent-categories

        for instance in session.query(Category).filter(Category.parent_id == ParentCategory.give_parent_categories(instance)[0]):
            table_budget.add_row(Category.give_info(instance))

        # Below code makes a visible break between parent categories (just for better readability of the table)
        table_budget.add_row([" ", " ", " ", " "])


    print(f"\nHere is your budget:")       # TODO: Here could be "Here is your budget called "{budget.name}"
    print("--------------------")
    print("MONTH: >>month<<")            # TODO: fill {month} with the right data (do f-string)
    print("--------------------")
    print(f"TOTAL BUDGETED:   {round(total_budgeted, 2)}        TO BE BUDGETED:   >>to_be_budgeted<<") # TODO: fill to_be_budgeted
    print(f"TOTAL ACTIVITY:   {round(total_activity, 2)}")
    print(f"TOTAL AVAILABLE:  {round(total_available, 2)}")

    print(table_budget)

    menu()


def new_transaction():
    print("\nNEW TRANSACTION MENU:")
    print("1. Inflow")
    print("2. Outflow")
    print(("## YOUR CHOICE: "))
    x = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")

    add_transaction()

def add_transaction():
    transaction_name = input("Write name of transaction: ")
    transaction_payee_name = input("Write name of payee/payer: ")
    transaction_amount_inflow = float(input("Inflow amount: "))
    transaction_amount_outflow = float(input("Outflow amount: "))
    transaction_category_id = int(input("Write category id: "))

    transaction = Transaction(name=transaction_name,
                                  payee_name=transaction_payee_name,
                                  amount_inflow=transaction_amount_inflow,
                                  amount_outflow=transaction_amount_outflow,
                                  category_id=transaction_category_id)
    session.add(transaction)
    session.commit()

    print_budget()


def edit_categories():
    print("\nEDIT CATEGORIES MENU:")
    print("   PARENT CATEGORY:")
    print("      1. Add parent category")
    print("      2. Remove parent category   [FUNCTION NOT AVAILABLE YET]")
    print("      3. Rename parent category   [FUNCTION NOT AVAILABLE YET]")
    print("   CATEGORY (subcategory of the parent category):")
    print("      4. Add category")
    print("      5. Remove category   [FUNCTION NOT AVAILABLE YET]")
    print("      6. Rename category   [FUNCTION NOT AVAILABLE YET]")
    print("")
    print("      7. Go back to the budget")
    choice = input("## YOUR CHOICE: ")

    if choice == "1":
        new_parent_category = input("Write name of new parent category: ")
        insert_into_parent_category_table = ParentCategory(name=new_parent_category, budget_id=budget_to_show)
        session.add(insert_into_parent_category_table)
        session.commit()
        print_budget()

    elif choice == "4":
        new_category = input("Write name of new category: ")
        which_parent_id = int(input("To which parent category does it belong (parent_id): "))
        new_budgeted_amount = float(input("Write budgeted amount: "))

        insert_into_category_table = Category(name=new_category, budgeted_amount=new_budgeted_amount, parent_id=which_parent_id)
        session.add(insert_into_category_table)
        session.commit()

        last_category_id = list(session.query(Category.id).order_by(Category.id.desc()).first())[0]
        empty_record = Transaction(name="# empty record", amount_inflow=0, amount_outflow=0, category_id=last_category_id)
        session.add(empty_record)
        session.commit()

        print_budget()

    elif choice == "7":
        print_budget()
    else:
        x = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")
        print_budget()

def edit_budget():
    print("\nEDIT BUDGET MENU:")
    print("@$@#%^@%@##@$%#^*&^ Here you edit budget (modify budgeted amounts)")
    x = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")

    print_budget()

def switch_month():
    print("\n@$@#%^@%@##@$%#^*&^ Here you can switch the month (the billing peroid)")
    x = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")

    print_budget()

def reports():
    print("\nREPORTS MENU:")
    print("0. Print the table with all transactions in this budget")
    print("1. Display the bar chart")
    print("2. Eksport my budget do csv file")
    print("3. Eksport my budget to json file")
    choice = input("## YOUR CHOICE: ")

    x = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")

    print_budget()

if __name__ == "__main__":
    change_user()

