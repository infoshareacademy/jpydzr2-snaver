from controllers.parentcategory_controller import add_parent_category
from controllers.parentcategory_controller import rename_parent_category
from models.Budget import Budget
from models.Category import Category
from prettytable import PrettyTable
from session import session

from models.CategoryBudget import CategoryBudget
from datetime import datetime

from calendar import monthrange

from enum import IntEnum

def menu_categories() -> str:
    print("\nEDIT CATEGORIES MENU:")
    print("   PARENT CATEGORY:")
    print("      1. Add parent category")
    print("      2. Remove parent category   [FUNCTION NOT AVAILABLE YET]")
    print("      3. Rename parent category")
    print("   CATEGORY (subcategory of the parent category):")
    print("      4. Add category")
    print("      5. Add budget to a category")
    print("      6. Rename category")
    print("    7. Go back to the budget")
    user_choice = input("## YOUR CHOICE: ")
    return int(user_choice)


def add_category() -> Category:
    category_name = input("The name of the new category: ")
    parent_id = int(input("To which parent category does it belong (parent_id): "))
    new_budgeted_amount = float(input("Write budgeted amount: "))
    category = Category(name=category_name, parent_id=parent_id)
    session.add(category)
    session.commit()
    # TODO: If more than one person creates a new category at the same time we might get incorrect data here
    new_category = session.query(Category).order_by(Category.id.desc()).first()
    category_budget = CategoryBudget(budgeted_amount=new_budgeted_amount, category_id=new_category.id,
                                     datetime=datetime.now())
    session.add(category_budget)
    session.commit()
    return new_category

class CategoryMenuEnums(IntEnum):
    PCADD = 1
    PCREMOVE = 2
    PCRENAME = 3
    CADD = 4
    BUDGETTOCAT = 5
    CRENAME = 6
    BACKTOBUDGET = 7

def edit_categories(budget, month, year):
    choice = menu_categories()

    if choice == CategoryMenuEnums.PCADD:
        _ = add_parent_category(budget)
    elif choice == CategoryMenuEnums.PCREMOVE:
        pass
    elif choice == CategoryMenuEnums.PCRENAME:
        _ = rename_parent_category(budget)
    elif choice == CategoryMenuEnums.CADD:
        _ = add_category()
    elif choice == CategoryMenuEnums.BUDGETTOCAT:
        _ = budget_category(budget, month, year)
    elif choice == CategoryMenuEnums.CRENAME:
        _ = rename_category(budget)
    elif choice == CategoryMenuEnums.BACKTOBUDGET:
        pass
    else:
        print(choice)
        _ = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")


def get_budget_categories(budget: Budget) -> list:
    all_categories = []
    all_parent_categories = [parent for parent in budget.parent_categories]
    for parent in all_parent_categories:
        for category in parent.categories:
            all_categories.append(category)

    return all_categories


def display_categories(budget: Budget) -> None:
    all_categories = get_budget_categories(budget)

    table_show_categories = PrettyTable()
    table_show_categories.field_names = ["id", "name"]

    for category in all_categories:
        table_show_categories.add_row([category.id, category.name])

    print("\nYour categories: ")
    print(table_show_categories)


def rename_category(budget: Budget) -> Category:
    all_categories = get_budget_categories(budget)
    display_categories(budget)
    choice = input("Pick category's ID to rename: ")

    selected_category = next((category for category in all_categories if category.id == int(choice)), None)
    if selected_category:
        new_name = input(f"Provide new name for {selected_category.name}: ")
        selected_category.name = new_name
        session.add(selected_category)
        session.commit()
        return selected_category
    else:
        print("Incorrect category!")


def budget_category(budget: Budget, month, year) -> Category:
    all_categories = get_budget_categories(budget)
    choice = input("Pick category's ID which you want to budget for this month: ")
    selected_category = next((category for category in all_categories if category.id == int(choice)), None)
    if selected_category:
        new_budget_amount = input("What amount do you wish to budget for this category: ")
        category_budget = session.query(CategoryBudget) \
            .filter(
            CategoryBudget.category_id == selected_category.id,
            CategoryBudget.datetime >= datetime(year, month, 1),
            CategoryBudget.datetime <= datetime(year, month, monthrange(year, month)[1])
        ).first()

        if category_budget:
            category_budget.budgeted_amount = new_budget_amount
            session.add(category_budget)
            session.commit()

        else:
            category_budget = CategoryBudget(budgeted_amount=new_budget_amount, category_id=selected_category.id,
                                             datetime=datetime(year, month, 1))
            session.add(category_budget)
            session.commit()
    else:
        print("Incorrect category!")
