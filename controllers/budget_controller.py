#from sqlalchemy.orm import lazyload

from models.Budget import Budget
from models.User import User
from models.Category import Category
from models.Transaction import Transaction
from models.ParentCategory import ParentCategory
from session import session
from prettytable import PrettyTable

from sqlalchemy import func


def add_budget(user: User) -> Budget:
    budget_name = input("Name of the new budget: ")
    budget = Budget(name=budget_name, user_id=user.id)
    session.add(budget)
    session.commit()
    new_budget = session.query(Budget).order_by(Budget.id.desc()).first()
    return new_budget


def select_budget(user: User) -> Budget:
    all_budgets = user.budgets
    if len(all_budgets) == 1:
        selected_budget = all_budgets[0]
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
    _ = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")
    return budget


def print_budget(budget: Budget) -> None:
    # Definition of PrettyTable
    table_budget = PrettyTable()
    table_budget.field_names = [" id, CATEGORY", "BUDGETED", "ACTIVITY", "AVAILABLE"]
    table_budget.align = "r"  # align in all columns to the right side
    table_budget.align[" id, CATEGORY"] = "l"  # align in column "CATEGORY" to the left side
    table_budget.float_format = "1.2"  # the way floating point data is printed

    # Reading data from database and inserting into PrettyTable
    total_budgeted = 0
    total_activity = 0
    total_available = 0

    for parent_instance in budget.parent_categories:
        # adding up values from categories and assigning them to parent_categories

        sum_budgeted = session.query(
            func.sum(Category.budgeted_amount)
            .filter(Category.parent_id == parent_instance.id)
            ).first()[0]

        sum_available = sum_budgeted - session.query(
            func.sum(Transaction.amount_outflow))\
            .join(Category).join(ParentCategory)\
            .filter(ParentCategory.id == parent_instance.id).first()[0]

        sum_activity = sum_budgeted - sum_available

        # Below code adds rows to PrettyTable like this:
        # | -------------------- | -------------------- | -------------------- | -------------------- |
        # | parent_category      |               xxx.xx |               yyy.yy |               zzz.zz |
        # | -------------------- | -------------------- | -------------------- | -------------------- |
        table_budget.add_row([30 * "-", 10 * "-", 10 * "-", 10 * "-"])
        table_budget.add_row(
            [f"[{parent_instance.id}, '{parent_instance.name}']", sum_budgeted, sum_activity, sum_available])
        table_budget.add_row([30 * "-", 10 * "-", 10 * "-", 10 * "-"])

        total_budgeted += sum_budgeted
        total_activity += sum_activity
        total_available += sum_available

        for category in parent_instance.categories:
            table_budget.add_row(category.fit_into_prettytable)

        # Below code makes a visible break between parent categories (just for better readability of the table)
        table_budget.add_row([" ", " ", " ", " "])

    print(
        f"\nHere is your budget \"{budget.name}\"")
    print("-----------------------------")
    print("MONTH: >>month<<")  # TODO: fill {month} with the right data (do f-string)
    print("-----------------------------")
    print(
        f"TOTAL BUDGETED:   {round(total_budgeted, 2)}        TO BE BUDGETED:   >>to_be_budgeted<<")  # TODO: fill to_be_budgeted
    print(f"TOTAL ACTIVITY:   {round(total_activity, 2)}")
    print(f"TOTAL AVAILABLE:  {round(total_available, 2)}")

    print(table_budget)


def print_budget_bar_chart(budget: Budget) -> None:
    bar_chart = PrettyTable()
    bar_chart.field_names = [" id, CATEGORY", "ACTIVITY", "BAR CHART"]
    bar_chart.align = "l"
    bar_chart.align["ACTIVITY"] = "r"
    bar_chart.float_format = "1.2"

    for parent_category_instance in budget.parent_categories:
        for category_instance in parent_category_instance.categories:
            activity_amount = sum(activity.amount_outflow for activity in category_instance.transactions)
            bar = int(round(activity_amount / 100)) * "#"  # Each 100 PLN is a single "#"
            bar_chart.add_row([(category_instance.id, category_instance.name), activity_amount, bar])
    print(bar_chart)
    _ = input("Press ENTER to go back.")
