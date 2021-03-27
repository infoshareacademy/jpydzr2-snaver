from session import session
from models.ParentCategory import ParentCategory
from models.Category import Category
from models.Transaction import Transaction


def edit_categories(budget):
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
    choice = input("## YOUR CHOICE: ")

    if choice == "1":
        new_parent_category = input("Write name of new parent category: ")
        insert_into_parent_category_table = ParentCategory(name=new_parent_category, budget_id=budget.id)
        session.add(insert_into_parent_category_table)
        session.commit()

    elif choice == "4":
        new_category = input("Write name of new category: ")
        which_parent_id = int(input("To which parent category does it belong (parent_id): "))
        new_budgeted_amount = float(input("Write budgeted amount: "))

        insert_into_category_table = Category(name=new_category, budgeted_amount=new_budgeted_amount,
                                              parent_id=which_parent_id)
        session.add(insert_into_category_table)
        session.commit()

        # Below we need to add empty record to Transactions to avoid errors during print_budget()
        last_category_id = list(session.query(Category.id).order_by(Category.id.desc()).first())[0]
        empty_record = Transaction(name="# empty record to initiate a new category", amount_inflow=0, amount_outflow=0,
                                   category_id=last_category_id)
        session.add(empty_record)
        session.commit()

    elif choice == "7":
        pass

    else:
        x = input("@$@#%^@%@##@$%#^*&^  WORK IN PROGRESS... Press ENTER to go back to your budget.")
