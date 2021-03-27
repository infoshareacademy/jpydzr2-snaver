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
    print("5. Switch the month (the billing period)")
    print("6. Reports")
    print("7. Change user")
    print("8. Save and close the program")
    choice = input("## YOUR CHOICE: ")
    return choice


def switch_month():
    print("\n@$@#%^@%@##@$%#^*&^ Here you can switch the month (the billing peroid)")
    x = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")


def reports(budget: Budget) -> None:
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
        for instance in session.query(ParentCategory).filter(ParentCategory.budget_id == budget.id):
            for value_budgeted in session.query(Category).filter(
                    Category.parent_id == ParentCategory.give_parent_categories(instance)[0]):
                activity_amount = Category.give_info(value_budgeted)[2]
                bar = int(round(activity_amount / 100)) * "#"  # The idea is that each 100 PLN is "#"
                bar_chart.add_row([Category.give_info(value_budgeted)[0], activity_amount, bar])
        print(bar_chart)
        x = input("press ENTER to go back to your budget")

    else:
        x = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")


def reading_ascii(file_name: str) -> None:
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip('\n')
            print(line)
