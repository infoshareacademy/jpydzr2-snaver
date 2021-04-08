from models.Transaction import Transaction
from session import session
from datetime import datetime


def add_transaction():
    transaction_name = input("Write name of transaction: ")
    transaction_payee_name = input("Write name of payee/payer: ")
    transaction_amount_inflow = float(input("Inflow amount: "))
    transaction_amount_outflow = float(input("Outflow amount: "))
    transaction_category_id = int(input("Write category id: "))
    transaction_receipt_date = datetime.strptime(input("Write date of transaction (YYYY-MM-DD): "), '%Y-%m-%d').date()

    transaction = Transaction(name=transaction_name,
                              payee_name=transaction_payee_name,
                              amount_inflow=transaction_amount_inflow,
                              amount_outflow=transaction_amount_outflow,
                              category_id=transaction_category_id,
                              receipt_date=transaction_receipt_date)
    session.add(transaction)
    session.commit()
