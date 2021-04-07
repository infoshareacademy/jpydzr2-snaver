from controllers.budget_controller import print_budget_bar_chart
from models.Budget import Budget
from datetime import datetime
from models.Transaction import Transaction
from session import session
from prettytable import PrettyTable


def menu_reports() -> str:
    print("\nREPORTS MENU:")
    print("1. Display the bar chart")
    print("2. Display all transactions in this budget   [FUNCTION NOT AVAILABLE YET]")
    print("3. Export my budget do csv file   [FUNCTION NOT AVAILABLE YET]")
    print("4. Export my budget to json file  [FUNCTION NOT AVAILABLE YET]")
    print("5. Filter transactions by receipt date ")
    choice = input("## YOUR CHOICE: ")
    return choice


def filter_by_receipt_date(budget: Budget) -> None:
    transaction_table = PrettyTable()
    transaction_table.field_names = ["Name", "Payee Name", "Inflow", "Outflow", "Category", "Receipt Date"]
    transaction_table.align = "l"
    transaction_table.float_format = "1.2"

    date_input = input("Write date for which you would like to check transactions (YYYY-MM-DD): ")
    transaction_time = datetime.strptime(date_input, '%Y-%m-%d').date()
    all_transactions = budget.all_transactions()

    for transaction in all_transactions:
        if transaction.receipt_date == transaction_time:
            name = transaction.name
            payee_name = transaction.payee_name
            inflow = transaction.amount_inflow
            outflow = transaction.amount_outflow
            category = transaction.category_id
            receipt_date = transaction.receipt_date
            transaction_table.add_row([name, payee_name, inflow, outflow, category, receipt_date])

    print(transaction_table)
    _ = input("Press ENTER to go back.")


def reports(budget: Budget) -> None:
    choice = menu_reports()

    if choice == "1":
        print_budget_bar_chart(budget)
    elif choice == "5":
        filter_by_receipt_date(budget)
    else:
        _ = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")
