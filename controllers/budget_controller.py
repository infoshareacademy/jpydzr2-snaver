from sqlalchemy.orm import lazyload

from models.Budget import Budget
from models.User import User
from models.Category import Category
from models.ParentCategory import ParentCategory
from session import session
from prettytable import PrettyTable


def add_budget(user: User) -> Budget:
    budget_name = input("Name of the new budget: ")
    budget = Budget(name=budget_name, user_id=user.id)
    session.add(budget)
    session.commit()
    new_budget = session.query(Budget).order_by(Budget.id.desc()).first()
    return new_budget


def select_budget(user: User) -> Budget:
    budgets = user.budgets
    if len(budgets) == 1:
        selected_budget = budgets[0]
    else:
        selected_budget = change_budget(user)
    return selected_budget


def change_budget(user: User) -> Budget:
    all_budgets = user.budgets

    table_show_budgets = PrettyTable()
    table_show_budgets.field_names = ["id", "name"]

    for budget_instance in all_budgets:
        table_show_budgets.add_row([budget_instance.id, budget_instance.name])

    while True:
        print("\nYour budgets: ")
        print(table_show_budgets)

        choice = input("Which budget to show? Pick budget's ID or input 'n' to create a new budget: ")
        if choice == 'n':
            selected_budget = add_budget(user)
        else:
            selected_budget = next((budget for budget in all_budgets if budget.id == int(choice)), None)
        if selected_budget:
            return selected_budget
        else:
            print("Select a correct budget!")


def edit_budget(budget: Budget) -> Budget:
    print("\nEDIT BUDGET MENU:")
    print("@$@#%^@%@##@$%#^*&^ Here you edit budget (modify budgeted amounts)")
    x = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")


def print_budget(budget: Budget) -> None:
    # Definition of PrettyTable
    table_budget = PrettyTable()
    table_budget.field_names = [" id, CATEGORY", "BUDGETED", "ACTIVITY", "AVAILABLE"]
    table_budget.align = "r"  # align in all columns to the right side
    table_budget.align[" id, CATEGORY"] = "l"  # align in column "CATEGORY" to the left side
    table_budget.float_format = "1.2"  # the way floating point data is printed

    # Reading data from database and inserting into PrettyTable
    sum_budgeted = 0
    sum_available = 0
    total_budgeted = 0
    total_activity = 0
    total_available = 0

    for parent_instance in budget.parent_categories:
        # adding up values from categories and assigning them to parent_categories
        for value_budgeted in session.query(Category).filter(
                Category.parent_id == ParentCategory.give_parent_categories(parent_instance)[0]):
            sum_budgeted += (Category.give_info(value_budgeted)[1])

        for value_available in session.query(Category).filter(
                Category.parent_id == ParentCategory.give_parent_categories(parent_instance)[0]):
            sum_available += (Category.give_info(value_available)[3])

        sum_activity = sum_budgeted - sum_available

        # Below code adds rows to PrettyTable like this:
        # | -------------------- | -------------------- | -------------------- | -------------------- |
        # | parent_category      |               xxx.xx |               yyy.yy |               zzz.zz |
        # | -------------------- | -------------------- | -------------------- | -------------------- |
        table_budget.add_row([30 * "-", 10 * "-", 10 * "-", 10 * "-"])
        table_budget.add_row(
            [ParentCategory.give_parent_categories(parent_instance), sum_budgeted, sum_activity, sum_available])
        table_budget.add_row([30 * "-", 10 * "-", 10 * "-", 10 * "-"])

        total_budgeted += sum_budgeted
        total_activity += sum_activity
        total_available += sum_available

        sum_budgeted = 0  # this is reset to zero to allow summing categories in next parent-categories
        sum_available = 0  # this is reset to zero to allow summing categories in next parent-categories

        for category_instance in parent_instance.categories:
            table_budget.add_row(Category.give_info(category_instance))

        # Below code makes a visible break between parent categories (just for better readability of the table)
        table_budget.add_row([" ", " ", " ", " "])

    print(
        f"\nHere is your budget \"{budget.name}\"")  # TODO: Here could be "Here is your budget called "{budget.name}"
    print("-----------------------------")
    print("MONTH: >>month<<")  # TODO: fill {month} with the right data (do f-string)
    print("-----------------------------")
    print(
        f"TOTAL BUDGETED:   {round(total_budgeted, 2)}        TO BE BUDGETED:   >>to_be_budgeted<<")  # TODO: fill to_be_budgeted
    print(f"TOTAL ACTIVITY:   {round(total_activity, 2)}")
    print(f"TOTAL AVAILABLE:  {round(total_available, 2)}")

    print(table_budget)


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
