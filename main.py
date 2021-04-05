"""File that starts the program"""

from controllers.user_controller import login
from controllers.budget_controller import print_budget, select_budget, change_budget, edit_budget
from controllers.category_controller import edit_categories
from controllers.transaction_controller import add_transaction
from controllers.reports_controller import reports

from datetime import datetime

month = datetime.now().month
year = datetime.now().year


def switch_month():
    # print("\n@$@#%^@%@##@$%#^*&^ Here you can switch the month (the billing period)")
    global month
    global year
    month = int(input("Month: "))
    year = int(input("Year: "))


def menu() -> str:
    print("MENU:")
    print("1. Change budget")
    print("2. New transaction (activity)")
    print("3. Edit categories")
    print("4. Edit budget (modify budgeted amounts)")
    print("5. Switch the month (the billing period)")
    print("6. Reports")
    print("7. Change user")
    print("8. Save and close the program")
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
            budget = change_budget(user)
        elif choice == "2":
            add_transaction()
        elif choice == "3":
            edit_categories(budget)
        elif choice == "4":
            budget = edit_budget(budget)
        elif choice == "5":
            switch_month()
        elif choice == "6":
            reports(budget)
        elif choice == "7":
            user = login()
            budget = select_budget(user)
        elif choice == "8":
            print(farewell_message)
            exit()

except KeyboardInterrupt:
    print(farewell_message)
    exit(0)
