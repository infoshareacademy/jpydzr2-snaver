from controllers.budget_controller import print_budget_bar_chart
from models.Budget import Budget
from datetime import datetime
from models.Transaction import Transaction
from session import session


def menu_reports() -> str:
    print("\nREPORTS MENU:")
    print("1. Display the bar chart")
    print("2. Display all transactions in this budget   [FUNCTION NOT AVAILABLE YET]")
    print("3. Export my budget do csv file   [FUNCTION NOT AVAILABLE YET]")
    print("4. Export my budget to json file  [FUNCTION NOT AVAILABLE YET]")
    print("5. Filter transactions by receipt date  [WORK IN PROGRESS]") # funkcja filtered_by_receipt_date ponizej - czy tutaj to dobry plik?
    choice = input("## YOUR CHOICE: ")
    return choice


def filter_by_receipt_date():
    date_input = input("Write date for which you would like to check transactions (YYYY-MM-DD): ")
    transaction_time = datetime.strptime(date_input, '%Y-%m-%d').date()
    filtered_by_date = session.query(Transaction).filter(Transaction.receipt_date == transaction_time).all()
    return filtered_by_date


def reports(budget: Budget) -> None:
    choice = menu_reports()

    if choice == "1":
        print_budget_bar_chart(budget)
    elif choice == "5":
        print(filter_by_receipt_date())
    else:
        _ = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")



