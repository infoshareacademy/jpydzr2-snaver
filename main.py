"""File that starts the program"""

from interface import *
from controllers.user_controller import login
from controllers.budget_controller import print_budget
from controllers.transaction_controller import add_transaction

welcome_message = "\nWelcome to Snaver!"
farewell_message = "\nGood bye!"

reading_ascii('docs/images/ascii_image_2.txt')
print(welcome_message)

try:
    user_id, user_name = login()
    while not user_id or not user_name:
        user_id, user_name = login()
    budget_id = select_budget(user_id)
    while True:
        print_budget(budget_id)
        choice = menu()

        if choice == "1":
            budget_id = change_budget(user_id)
        elif choice == "2":
            add_transaction()
        elif choice == "3":
            edit_categories(budget_id)
        elif choice == "4":
            edit_budget()
        elif choice == "5":
            switch_month()
        elif choice == "6":
            reports(budget_id)
        elif choice == "7":
            user_id, user_name = login()
            budget_id = select_budget(user_id)
        elif choice == "8":
            print(farewell_message)
            exit()
    
except KeyboardInterrupt as keyboard_exit:
    print(farewell_message)
    exit(0)
