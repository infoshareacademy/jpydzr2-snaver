from models.Budget import Budget
from models.Category import Category
from models.ParentCategory import ParentCategory
from models.Transaction import Transaction
from models.User import User
from controllers.budget_controller import *


from session import session

from prettytable import PrettyTable


def menu():
    print("MENU:")
    print("1. Change budget")
    print("2. New transaction (activity)")
    print("3. Edit categories")
    print("4. Edit budget (modify budgeted amounts)")
    print("5. Switch the month (the billing peroid")
    print("6. Reports")
    print("7. Change user")
    print("8. Save and close the program")
    choice = input("## YOUR CHOICE: ")
    return choice

def edit_categories(budget_id):
    print("\nEDIT CATEGORIES MENU:")
    print("   PARENT CATEGORY:")
    print("      1. Add parent category")
    print("      2. Remove parent category   [FUNCTION NOT AVAILABLE YET]")
    print("      3. Rename parent category   [FUNCTION NOT AVAILABLE YET]")
    print("   CATEGORY (subcategory of the parent category):")
    print("      4. Add category")
    print("      5. Remove category   [FUNCTION NOT AVAILABLE YET]")
    print("      6. Rename category   [FUNCTION NOT AVAILABLE YET]")
    print("    7. Go back to the budget")
    choice = input("## YOUR CHOICE: ")

    if choice == "1":
        new_parent_category = input("Write name of new parent category: ")
        insert_into_parent_category_table = ParentCategory(name=new_parent_category, budget_id=budget_id)
        session.add(insert_into_parent_category_table)
        session.commit()

    elif choice == "4":
        new_category = input("Write name of new category: ")
        which_parent_id = int(input("To which parent category does it belong (parent_id): "))
        new_budgeted_amount = float(input("Write budgeted amount: "))

        insert_into_category_table = Category(name=new_category, budgeted_amount=new_budgeted_amount,
                                              parent_id=which_parent_id)
        session.add(insert_into_category_table)
        session.commit()

        # Below we need to add empty record to Transactions to avoid errors during print_budget()
        last_category_id = list(session.query(Category.id).order_by(Category.id.desc()).first())[0]
        empty_record = Transaction(name="# empty record to initiate a new category", amount_inflow=0, amount_outflow=0,
                                   category_id=last_category_id)
        session.add(empty_record)
        session.commit()

    elif choice == "7":
        pass

    else:
        x = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")


def edit_budget():
    print("\nEDIT BUDGET MENU:")
    print("@$@#%^@%@##@$%#^*&^ Here you edit budget (modify budgeted amounts)")
    x = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")


def switch_month():
    print("\n@$@#%^@%@##@$%#^*&^ Here you can switch the month (the billing peroid)")
    x = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")


def reports(budget_id):
    print("\nREPORTS MENU:")
    print("0. Print the table with all transactions in this budget   [FUNCTION NOT AVAILABLE YET]")
    print("1. Display the bar chart")
    print("2. Eksport my budget do csv file   [FUNCTION NOT AVAILABLE YET]")
    print("3. Eksport my budget to json file  [FUNCTION NOT AVAILABLE YET]")
    choice = input("## YOUR CHOICE: ")

    if choice == "1":
        # Definition of PrettyTable
        bar_chart = PrettyTable()
        bar_chart.field_names = [" id, CATEGORY", "ACTIVITY", "BAR CHART"]
        bar_chart.align = "l"  # align in all columns to the left side
        bar_chart.align["ACTIVITY"] = "r"  # align in column "ACTIVITY" to the right side
        bar_chart.float_format = "1.2"  # the way floating point data is printed, for example "123.45"

        # reading values from database and inserting into PrettyTable
        for instance in session.query(ParentCategory).filter(ParentCategory.budget_id == budget_id):
            for value_budgeted in session.query(Category).filter(
                    Category.parent_id == ParentCategory.give_parent_categories(instance)[0]):
                activity_amount = Category.give_info(value_budgeted)[2]
                bar = int(round(activity_amount / 100)) * "#"  # The idea is that each 100 PLN is "#"
                bar_chart.add_row([Category.give_info(value_budgeted)[0], activity_amount, bar])
        print(bar_chart)
        x = input("press ENTER to go back to your budget")

    else:
        x = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")


def reading_ascii(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip('\n')
            print(line)
