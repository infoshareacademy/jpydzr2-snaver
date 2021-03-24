from session import session

from models.ParentCategory import ParentCategory
from models.ParentCategory import ParentCategoryNotFoundException


def update_parent_category_name(parent_category_id: int, new_name: str):
    category_instance = session.query(ParentCategory).filter_by(id=parent_category_id).first()
    if category_instance:
        category_instance.name = new_name
        session.commit()
        return category_instance
    else:
        raise ParentCategoryNotFoundException(parent_category_id)
