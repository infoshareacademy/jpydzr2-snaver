from controllers.budget_controller import print_budget_bar_chart
from models.Budget import Budget


def menu_reports() -> str:
    print("\nREPORTS MENU:")
    print("1. Display the bar chart")
    print("2. Display all transactions in this budget   [FUNCTION NOT AVAILABLE YET]")
    print("3. Export my budget do csv file   [FUNCTION NOT AVAILABLE YET]")
    print("4. Export my budget to json file  [FUNCTION NOT AVAILABLE YET]")
    choice = input("## YOUR CHOICE: ")
    return choice


def reports(budget: Budget) -> None:
    choice = menu_reports()

    if choice == "1":
        print_budget_bar_chart(budget)
    else:
        _ = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")
