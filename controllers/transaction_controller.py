from sqlalchemy.orm import lazyload

from models.Budget import Budget
from models.Transaction import Transaction
from session import session


def add_transaction():
    transaction_name = input("Podaj nazwe transakcji: ")
    transaction_payee_name = input("Podaj nazwę sklepu lub płatnika: ")
    transaction_amount_inflow = float(input("Podaj kwotę wpływu: "))
    transaction_amount_outflow = float(input("Podaj kwotę wydatku: "))
    transaction_category_id = int(input("Podaj id kategorii: "))

    transaction = Transaction(name=transaction_name,
                              payee_name=transaction_payee_name,
                              amount_inflow=transaction_amount_inflow,
                              amount_outflow=transaction_amount_outflow,
                              category_id=transaction_category_id)
    session.add(transaction)
    session.commit()
