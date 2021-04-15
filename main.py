"""File that starts the program"""

from controllers.budget_controller import edit_budget
from controllers.budget_controller import print_budget
from controllers.budget_controller import select_budget
from controllers.category_controller import edit_categories
from controllers.reports_controller import reports
from controllers.transaction_controller import add_transaction
from controllers.user_controller import login
from styles.styles import style
from datetime import datetime

from enum import IntEnum


def switch_month():
    global month
    global year

    while True:
        try:
            input_month = int(input("Month (number of the month): "))
            input_year = int(input("Year: "))
        except ValueError:
            print("Sorry, I did not understand this")
            continue
        if not 12 >= input_month >= 1 or not year + 2 >= input_year >= year - 2:
            print("Oops, wrong date! Try again.")
            continue
        else:
            month = input_month
            year = input_year
            break

def menu() -> str:
    print("MENU:")
    print("1. New transaction")
    print("2. Edit categories")
    print("3. Edit budgets")
    print("4. Switch the month (the billing period)")
    print("5. Reports")
    print("6. Change user")
    print("7. Close the program")
    user_choice = input("## YOUR CHOICE: ")
    return int(user_choice)


def reading_ascii(file_name: str) -> None:
    print(f"{style.tBLUE}")
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip('\n')
            print(line)
    print(f"{style.RESET}")


welcome_message = "\nWelcome to Snaver!"
farewell_message = "\nGood bye!"

month = datetime.now().month
year = datetime.now().year

reading_ascii('docs/images/ascii_image_2.txt')
print(welcome_message)

class MainMenuEnums(IntEnum):
    NEWTRANSACTION = 1
    EDITCAT = 2
    EDITBUDGET = 3
    SWITCHMONTH = 4
    REPORTS = 5
    CHANGEUSER = 6
    CLOSE = 7

try:
    user = login()
    while not user:
        user = login()
    budget = select_budget(user)
    while True:
        print_budget(budget, month, year)
        choice = menu()

        if choice == MainMenuEnums.NEWTRANSACTION:
            _ = add_transaction(budget)
        elif choice == MainMenuEnums.EDITCAT:
            edit_categories(budget, month, year)
        elif choice == MainMenuEnums.EDITBUDGET:
            edited_budget = edit_budget(user)
            if edited_budget:
                budget = edited_budget
        elif choice == MainMenuEnums.SWITCHMONTH:
            switch_month()
        elif choice == MainMenuEnums.REPORTS:
            reports(budget)
        elif choice == MainMenuEnums.CHANGEUSER:
            new_user = login()
            if new_user:
                user = new_user
                budget = select_budget(user)
        elif choice == MainMenuEnums.CLOSE:
            print(farewell_message)
            exit(0)

except KeyboardInterrupt:
    print(farewell_message)
    exit(0)
