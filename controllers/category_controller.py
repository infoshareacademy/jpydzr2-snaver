from models.Category import Category
from models.Category import CategoryNotFoundException
from session import session


def update_category_name(category_id: int, new_name: str):
    category_instance = session.query(Category).filter_by(id=category_id).first()
    if category_instance:
        category_instance.name = new_name
        session.commit()
        return category_instance
    else:
        raise CategoryNotFoundException(category_id)
