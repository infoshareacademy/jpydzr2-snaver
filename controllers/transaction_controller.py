from sqlalchemy.orm import lazyload

from models.Budget import Budget
from models.Transaction import Transaction
from session import session



def add_transaction():
    transaction_name = input("Write name of transaction: ")
    transaction_payee_name = input("Write name of payee/payer: ")
    transaction_amount_inflow = float(input("Inflow amount: "))
    transaction_amount_outflow = float(input("Outflow amount: "))
    transaction_category_id = int(input("Write category id: "))

    transaction = Transaction(name=transaction_name,
                                  payee_name=transaction_payee_name,
                                  amount_inflow=transaction_amount_inflow,
                                  amount_outflow=transaction_amount_outflow,
                                  category_id=transaction_category_id)
    session.add(transaction)
    session.commit()

    print_budget()