#from sqlalchemy.orm import lazyload

from models.Budget import Budget
from models.User import User
from models.Category import Category
from models.Transaction import Transaction
from models.ParentCategory import ParentCategory
from session import session
from prettytable import PrettyTable
from styles.style import style


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

    for budget in all_budgets:
        table_show_budgets.add_row([budget.id, budget.name])

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
    # Initiate and set up a PrettyTable table
    table_budget = PrettyTable()
    table_budget.field_names = ["id, CATEGORY", "BUDGETED", "ACTIVITY", "AVAILABLE"]
    table_budget.align = "r"  # align in all columns to the right side
    table_budget.align["id, CATEGORY"] = "l"  # align in column "CATEGORY" to the left side
    table_budget.float_format = "1.2"  # the way floating point data is printed

    # Loop through parent categories of the budget
    for parent in budget.parent_categories:

        # Code belows adds rows to PrettyTable object (table_budget)
        # | -------------------- | -------------------- | -------------------- | -------------------- |
        # | parent_category      |               xxx.xx |               yyy.yy |               zzz.zz |
        # | -------------------- | -------------------- | -------------------- | -------------------- |

        # Start drawing the lines
        table_budget.add_row([40 * "-", 10 * "-", 10 * "-", 10 * "-"])

        # Fill the row with parent's details using prettytable_repr method
        table_budget.add_row(parent.prettytable_repr)

        # Draw closing lines
        table_budget.add_row([40 * "-", 10 * "-", 10 * "-", 10 * "-"])

        # Attach category details as new rows
        for category in parent.categories:
            table_budget.add_row(category.prettytable_repr)

        # Draw blank row before the new Parent row (just for better readability of the table)
        table_budget.add_row([" ", " ", " ", " "])

    # Print budget headlines
    print(f"\n{style.tYELLOW}{style.fBOLD}{style.fUNDERLINE}")
    print(f"Here is your budget \"{budget.name}\"{style.RESET}")
    print(f"{style.tYELLOW}{style.fUNDERLINE}MONTH: >>month<<{style.RESET}")  # TODO: fill {month} with the right data

    head_table = PrettyTable()
    head_table.add_column("TO BE BUDGETED", [
        "",
        f" TO BE BUDGETED: >>to_be_budg<<         ",  # TODO: fill {to_be_budg}
        f" INFLOWS: >>inflows<<"             # TODO: fill {inflows}
    ])
    head_table.add_column("TOTAL BUDGETED", [
        f"    TOTAL   ",
        f"    BUDGETED",
        f"%.2f" % budget.total_budgeted
    ])
    head_table.add_column("TOTAL ACTIVITY", [
        f"   TOTAL   ",
        f"   ACTIVITY",
        f"%.2f" % budget.total_activity
    ])
    head_table.add_column("TOTAL AVAILABLE", [
        f"  TOTAL    ",
        f"  AVAILABLE",
        f"%.2f" % (budget.total_budgeted + budget.total_activity)
    ])
    # NOTE: Above '%.2f' is made for printing two decimal places including zeros at the end.
    # (When we use "round(x, 2) then it prints for example 7.0 instead of 7.00)

    head_table.align = "r"
    head_table.align["TO BE BUDGETED"] = "l"
    head_table.header = False
    head_table.border = False

    print(f"{style.tYELLOW}", end="")   # end="" causes that there is no empty newline after this line of code.
    print(head_table, end="")
    print(f"{style.RESET}")


    # Print the table
    print(table_budget)


def print_budget_bar_chart(budget: Budget) -> None:
    bar_chart = PrettyTable()
    bar_chart.field_names = ["id, CATEGORY", "ACTIVITY", "BAR CHART"]
    bar_chart.align = "l"
    bar_chart.align["ACTIVITY"] = "r"
    bar_chart.float_format = "1.2"

    i_color = 31
    for parent in budget.parent_categories:
        for category in parent.categories:
            activity_amount = sum(activity.amount_outflow for activity in category.transactions)
            bar = int(round(activity_amount / 100)) * f"\033[{i_color}m█{style.RESET}"  # Each 100 PLN is a single "█"
            bar_chart.add_row([(category.id, category.name), activity_amount, bar])
            i_color += 1
            if i_color == 38:
                i_color = 31
    print(bar_chart)
    _ = input("Press ENTER to go back to your budget.")