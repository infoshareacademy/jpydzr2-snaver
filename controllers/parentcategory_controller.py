from models.Budget import Budget
from models.ParentCategory import ParentCategory
from prettytable import PrettyTable
from session import session


def add_parent_category(budget: Budget) -> ParentCategory:
    parent_category_name = input("The name of the new parent category: ")
    parent_category = ParentCategory(name=parent_category_name, budget_id=budget.id)
    session.add(parent_category)
    session.commit()
    new_parent_category = session.query(Budget).order_by(Budget.id.desc()).first()
    return new_parent_category


def display_parent_categories(budget: Budget) -> None:
    all_parent_categories = budget.parent_categories

    table_show_parents = PrettyTable()
    table_show_parents.field_names = ["id", "name"]

    for parent_category in all_parent_categories:
        table_show_parents.add_row([parent_category.id, parent_category.name])

    print("\nYour Parent categories: ")
    print(table_show_parents)


def rename_parent_category(budget: Budget) -> ParentCategory:
    display_parent_categories(budget)
    choice = input("Pick parent category's ID to rename: ")

    selected_parent = next((parent for parent in budget.parent_categories if parent.id == int(choice)), None)
    if selected_parent:
        new_name = input(f"Provide new name for {selected_parent.name}: ")
        selected_parent.name = new_name
        session.add(selected_parent)
        session.commit()
        return selected_parent
    else:
        print("Incorrect parent category!")
