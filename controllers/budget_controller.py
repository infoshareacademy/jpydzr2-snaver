from sqlalchemy.orm import lazyload

from models.Budget import Budget
from models.ParentCategory import ParentCategory
from session import session


# GLOBAL VARIABLES
global_user_id = None
global_user_name = None


# DEFINE LOGIC HERE

# Show user's budget
def show_budget():
    # refer to global variables inside function
    global global_user_id
    global global_user_name

    # Try to retrieve the user's budget
    budget_instance = session.query(Budget).filter_by(user_id=global_user_id).first()

    # If user has no budgets
    if budget_instance is None:
        print("\nWhoops, you don't have any budgets yet. Shall we create one?")
        add_budget()

    # else == User does have at least 1 budget
    else:
        # Welcome message
        print("\n{}, here's your budget!".format(global_user_name))

        # Get the list of all user's budgets and its children up to the category level
        budgets_list = session.query(Budget).filter_by(user_id=global_user_id).options(
            lazyload(Budget.parent_categories).subqueryload(ParentCategory.categories)).all()

        # Zapytanie wyżej zwraca listę budżetów zalogowanego użytkownika, w której są listy pod-dzieci
        # Wpisanie budgets_list[0].parent_categories zwraca listę parent kategorii pierwszego budżetu na liście
        # budgets_list[0].parent_categories[0].categories zwraca listę kategorii i tak dalej

        # print the name of the first budget on the list
        print("\n{}".format(budgets_list[0].name.upper()))  # Print first budget's name

        # LOAD WHOLE BUDGET

        # loop through parent categories of the first budget in the list
        for parent in budgets_list[0].parent_categories:

            # Start calculating the parent's available amount based its children' available_amount
            parent_available_sum = 0.00

            # Loop through the parent's categories to add available_amount to the parent_available_sum
            for category in parent.categories:
                parent_available_sum += category.available_amount

            # Format the result and print it along parent category's name
            formatted_sum = "{:.2f} zł".format(parent_available_sum)
            print("\n---------------- {}, dostępna kwota: {} ---------------- \n".format(parent.name, formatted_sum))

            # Loop through the categories of the parent ONCE AGAIN, this time to print them
            n = 1  # Position (number) of the category within the parent
            for category in parent.categories:
                formatted_available = "{:.2f} zł".format(category.available_amount)
                print("{}. {}, dostępne środki: {}".format(n, category.name, formatted_available))
                n += 1  # Increment the category number

        print("\n")  # Print space between the next command


def add_budget():
    global global_user_id
    budget_name = input("Nazwij swój budżet:")
    budget = Budget(name=budget_name, user_id=global_user_id)
    session.add(budget)
    session.commit()
    show_budget()

# Written by Robert:
def add_new_budget(user_to_show):
    budget_name = input("Name of new budget: ")
    budget = Budget(name=budget_name, user_id=user_to_show)
    session.add(budget)
    session.commit()
