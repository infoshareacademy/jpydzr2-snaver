"""File that starts the program"""

from interface import reading_ascii, menu, switch_month, reports
from controllers.user_controller import login
from controllers.budget_controller import print_budget, select_budget, change_budget, edit_budget
from controllers.category_controller import edit_categories
from controllers.transaction_controller import add_transaction

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
        print_budget(budget)
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
