from session import session



# ADD PARENT CATEGORIES
# ------------------------------

# parent_category_list = []
# parent_category_names = ["Rachunki", "Kredyty", "Wydatki na życie", "Odkładanie", "Rozrywki"]
#
# for budget_instance in session.query(Budget).order_by(Budget.id):
#     for i in range(len(parent_category_names)):
#         parent_category_list.append(ParentCategory(name=parent_category_names[i], budget_id=budget_instance.id))
#
# session.add_all(parent_category_list)
# session.commit()



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
