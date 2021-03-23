from sqlalchemy.orm import lazyload

from models.Budget import Budget
from models.Category import Category
from models.ParentCategory import ParentCategory
from session import session
from prettytable import PrettyTable

global global_user_id

# def menu(global_user_id):
#     print("MENU:")
#     print("0. Change user")
#     print("1. Change budget")
#     print("2. New transaction (activity)")
#     print("3. Edit categories")
#     print("4. Edit budget (modify budgeted amounts)")
#     print("5. Switch the month (the billing peroid")
#     print("6. Reports")
#     print("7. Save and close the program")
#     choice = input("## YOUR CHOICE: ")
#
#     if choice == "0":
#         change_user()
#     if choice == "1":
#         change_budget(global_user_id)
#     if choice == "2":
#         add_transaction()
#     if choice == "3":
#         edit_categories()
#     if choice == "4":
#         edit_budget()
#     if choice == "5":
#         switch_month()
#     if choice == "6":
#         reports()
#     if choice == "7":
#         print("End. Program closed.")
#         exit()
#     else:
#         print("\n!!! >>> WRONG CHOICE (OUT OF RANGE). TRY AGAIN...")
#         menu()


def add_budget(global_user_id):
    budget_name = input("Name of new budget: ")
    budget = Budget(name=budget_name, user_id=global_user_id)
    session.add(budget)
    session.commit()


def change_budget(global_user_id):
    print("\nYour budgetes:")

    ''' Printing the table with user's budgetes.'''
    # Definition of PrettyTable for budgetes.
    table_show_budgetes = PrettyTable()
    table_show_budgetes.field_names = ["id", "name"]

    # Reading data from databe and inserting into PrettyTable
    for instance in session.query(Budget).filter(Budget.user_id == global_user_id):
        table_show_budgetes.add_row([Budget.give_budgets(instance)[0], Budget.give_budgets(instance)[1]])

    print(table_show_budgetes)

    ''' Printing the budget's table that user selected.'''
    global budget_to_show
    # budget_to_show = input("Which budget to show? Input budget's id: ")
    budget_to_show = input("Which budget to show? Input budget's id OR input 'n' to create new budget: ")
    if budget_to_show == 'n':
        add_budget(global_user_id)
        budget_to_show = list(session.query(Budget.id).order_by(Budget.id.desc()).first())[0]
    print_budget(global_user_id)


def print_budget(global_user_id):
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


    print(f"\nHere is your budget >>id_{budget_to_show}<<:")       # TODO: Here could be "Here is your budget called "{budget.name}"
    print("-----------------------------")
    print("MONTH: >>month<<")            # TODO: fill {month} with the right data (do f-string)
    print("-----------------------------")
    print(f"TOTAL BUDGETED:   {round(total_budgeted, 2)}        TO BE BUDGETED:   >>to_be_budgeted<<") # TODO: fill to_be_budgeted
    print(f"TOTAL ACTIVITY:   {round(total_activity, 2)}")
    print(f"TOTAL AVAILABLE:  {round(total_available, 2)}")

    print(table_budget)
    # menu(global_user_id)
    return global_user_id


def reports(global_user_id):
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
        bar_chart.align["ACTIVITY"] = "r"   # align in column "ACTIVITY" to the right side
        bar_chart.float_format = "1.2"  # the way floating point data is printed, for example "123.45"

        # reading values from database and inserting into PrettyTable
        for instance in session.query(ParentCategory).filter(ParentCategory.budget_id == budget_to_show):
            for value_budgeted in session.query(Category).filter(Category.parent_id == ParentCategory.give_parent_categories(instance)[0]):
                activity_amount = Category.give_info(value_budgeted)[2]
                bar = int(round(activity_amount/100)) * "#"     # The idea is that each 100 PLN is "#"
                bar_chart.add_row([Category.give_info(value_budgeted)[0], activity_amount, bar])
        print(bar_chart)
        x = input("press ENTER to go back to your budget")

    else:
        x = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")

    print_budget(global_user_id)

