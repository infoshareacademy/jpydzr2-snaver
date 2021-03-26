"""File that starts the program"""

from interface import *

welcome_message = "\nWelcome to Snaver!"
farewell_message = "\nGood bye!"
close_snaver = False

reading_ascii('docs/images/ascii_image_2.txt')
print(welcome_message)

try:
    user_id, user_name = login()
    while not user_id or not user_name:
        user_id, user_name = login()
    budget_id = select_budget(user_id)
    while not close_snaver:
        print_budget(budget_id)
        choice = menu(user_id)

        if choice == "1":
            budget_id = change_budget(user_id)
        elif choice == "2":
            add_transaction()
        elif choice == "3":
            edit_categories()
        elif choice == "4":
            edit_budget()
        elif choice == "5":
            switch_month()
        elif choice == "6":
            reports()
        elif choice == "7":
            user_id, user_name = login()
        elif choice == "8":
            print("Good bye!")
            exit()
    print(farewell_message)
except KeyboardInterrupt as keyboard_exit:
    print(farewell_message)
    exit(0)
