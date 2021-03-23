"""Package that is responsible for application's internal logic

It is induced by main.py
"""

from controllers.base_controller import *
from controllers.budget_controller import *
from controllers.category_controller import *
from controllers.parentcategory_controller import *
from controllers.transaction_controller import *
from controllers.user_controller import *
from prettytable import PrettyTable


global global_user_id

def menu(global_user_id):
    print(f"glob user id: {global_user_id}")
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
        global login
        login = login()
        global_user_id = login[0]
        change_budget(global_user_id)
        # change_user()
    if choice == "1":
        change_budget(global_user_id)
    if choice == "2":
        add_transaction()
    if choice == "3":
        edit_categories()
    if choice == "4":
        edit_budget()
    if choice == "5":
        switch_month()
    if choice == "6":
        reports(global_user_id)
    if choice == "7":
        print("End. Program closed.")
        exit()
    else:
        print("\n!!! >>> WRONG CHOICE (OUT OF RANGE). TRY AGAIN...")
        menu(global_user_id)


change_budget(global_user_id)
# TODO zamiast powyższej linijki zrobić if:
#  jeśli użytkownik ma tylko jeden budzet: print_budget(budget_id) "first"
#  jeśli użytkownik ma więcej niż jeden budzet: change_budget(global_user_id)

menu(global_user_id)



