from models.Budget import Budget
from models.ParentCategory import ParentCategory
from models.ParentCategory import ParentCategoryNotFoundException
from session import session


def add_parent_category(budget: Budget) -> ParentCategory:
    parent_category_name = input("The name of the new parent category: ")
    parent_category = ParentCategory(name=parent_category_name, budget_id=budget.id)
    session.add(parent_category)
    session.commit()
    new_parent_category = session.query(Budget).order_by(Budget.id.desc()).first()
    return new_parent_category


def edit_categories():
    print("\nEDIT CATEGORIES MENU:")
    print("   PARENT CATEGORY:")
    print("      1. Add parent category")
    print("      2. Remove parent category")
    print("      3. Rename parent category")
    print("   CATEGORY (subcategory of the parent category):")
    print("      4. Add category")
    print("      5. Remove category")
    print("      6. Rename category")
    print("## YOUR CHOICE: ")
    x = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")


def update_parent_category_name(parent_category_id: int, new_name: str):
    parent_category_instance = session.query(ParentCategory).filter_by(id=parent_category_id).first()
    if parent_category_instance:
        parent_category_instance.name = new_name
        session.commit()
        return parent_category_instance
    else:
        raise ParentCategoryNotFoundException(parent_category_id)
