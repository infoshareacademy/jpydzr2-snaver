from session import session
from models.Category import Category
from controllers.parentcategory_controller import add_parent_category
from models.CategoryBudget import CategoryBudget

from datetime import datetime


def menu_categories() -> str:
    print("\nEDIT CATEGORIES MENU:")
    print("   PARENT CATEGORY:")
    print("      1. Add parent category")
    print("      2. Remove parent category   [FUNCTION NOT AVAILABLE YET]")
    print("      3. Rename parent category   [FUNCTION NOT AVAILABLE YET]")
    print("   CATEGORY (subcategory of the parent category):")
    print("      4. Add category")
    print("      5. Remove category   [FUNCTION NOT AVAILABLE YET]")
    print("      6. Rename category   [FUNCTION NOT AVAILABLE YET]")
    print("    7. Go back to the budget")
    user_choice = input("## YOUR CHOICE: ")
    return user_choice


def add_category() -> Category:
    category_name = input("The name of the new parent category: ")
    parent_id = int(input("To which parent category does it belong (parent_id): "))
    new_budgeted_amount = float(input("Write budgeted amount: "))
    category = Category(name=category_name, parent_id=parent_id)
    session.add(category)
    session.commit()
    # TODO: If more than one person creates a new category at the same time we might get incorrect data here
    new_category = session.query(Category).order_by(Category.id.desc()).first()
    category_budget = CategoryBudget(budgeted_amount=new_budgeted_amount, category_id=new_category.id, datetime=datetime.now())
    session.add(category_budget)
    session.commit()
    return new_category


def edit_categories(budget):
    choice = menu_categories()

    if choice == "1":
        _ = add_parent_category(budget)

    elif choice == "4":
        _ = add_category()

    elif choice == "7":
        pass

    else:
        x = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")
