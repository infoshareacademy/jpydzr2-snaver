from models.Transaction import Transaction
from models.Budget import Budget

from session import session
from datetime import datetime


def add_transaction(budget: Budget) -> bool:
    name = input("Name of the transaction: ")
    try:
        outflow = float(input("Outflow amount: ") or 0.)

        if outflow == 0.:
            inflow = float(input("Inflow amount: "))
        else:
            inflow = 0.

        category_id = int(input("Category id: "))
        valid_ids = []
        for parent in budget.parent_categories:
            for category in parent.categories:
                valid_ids.append(category.id)

        if category_id not in valid_ids:
            print("Invalid category ID!")
            return False

        provided_date = input("Date of the transaction (YYYY-MM-DD): ")

        if provided_date:
            receipt_date = datetime.strptime(provided_date, '%Y-%m-%d').date()
        else:
            receipt_date = datetime.today().date()

        payee_name = input("Name of payee/payer: ")

    except ValueError:
        print("You provided an incorrect value!")
        return False

    transaction = Transaction(name=name,
                              payee_name=payee_name,
                              amount_inflow=inflow,
                              amount_outflow=outflow,
                              category_id=category_id,
                              receipt_date=receipt_date)
    session.add(transaction)
    session.commit()
    print("The transaction has been added!")

    return True
