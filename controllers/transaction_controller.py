from models.Transaction import Transaction
from session import session
from datetime import datetime


def add_transaction():
    name = input("Write name of transaction: ")
    outflow = float(input("Outflow amount: ") or 0.)

    if outflow == 0.:
        inflow = float(input("Inflow amount: "))
    else:
        inflow = 0.

    category_id = int(input("Category id: "))
    provided_date = input("Date of the transaction (YYYY-MM-DD): ")

    if provided_date:
        receipt_date = datetime.strptime(provided_date, '%Y-%m-%d').date()
    else:
        receipt_date = datetime.today().date()

    payee_name = input("Write name of payee/payer: ")

    transaction = Transaction(name=name,
                              payee_name=payee_name,
                              amount_inflow=inflow,
                              amount_outflow=outflow,
                              category_id=category_id,
                              receipt_date=receipt_date)
    session.add(transaction)
    session.commit()
