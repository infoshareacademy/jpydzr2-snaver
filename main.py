"""File that starts the program"""

from controllers.budget_controller import edit_budget
from controllers.budget_controller import print_budget
from controllers.budget_controller import select_budget
from controllers.category_controller import edit_categories
from controllers.reports_controller import reports
from controllers.transaction_controller import add_transaction
from controllers.user_controller import login

from datetime import datetime

month = datetime.now().month
year = datetime.now().year


def switch_month():
    # print("\n@$@#%^@%@##@$%#^*&^ Here you can switch the month (the billing period)")
    global month
    global year
    month = int(input("Month (number of the month): "))
    year = int(input("Year: "))


def menu() -> str:
    print("MENU:")
    print("1. New transaction (activity)")
    print("2. Edit categories")
    print("3. Edit budgets")
    print("4. Switch the month (the billing period)")
    print("5. Reports")
    print("6. Change user")
    print("7. Close the program")
    user_choice = input("## YOUR CHOICE: ")
    return user_choice


def reading_ascii(file_name: str) -> None:
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip('\n')
            print(line)


welcome_message = "\nWelcome to Snaver!"
farewell_message = "\nGood bye!"

reading_ascii('docs/images/ascii_image_2.txt')
print(welcome_message)

try:
    user = login()
    while not user:
        user = login()
    budget = select_budget(user)
    while True:
        print_budget(budget, month, year)
        choice = menu()

        if choice == "1":
            add_transaction()
        elif choice == "2":
            edit_categories(budget)
        elif choice == "3":
            edited_budget = edit_budget(user)
            if edited_budget:
                budget = edited_budget
        elif choice == "4":
            switch_month()
        elif choice == "5":
            reports(budget)
        elif choice == "6":
            new_user = login()
            if new_user:
                user = new_user
                budget = select_budget(user)
        elif choice == "7":
            print(farewell_message)
            exit(0)

except KeyboardInterrupt:
    print(farewell_message)
    exit(0)
