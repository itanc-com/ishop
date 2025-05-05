from sqlalchemy.orm import Session

from app.modules.category.models import Category


class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, title: str, parent_id: int = None) -> Category:
        category = Category(title=title, parent_id=parent_id)
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        return category

    def get_by_id(self, category_id: int) -> Category | None:
        return self.session.query(Category).filter(Category.id == category_id).first()

    def list_all(self) -> list[Category]:
        return self.session.query(Category).all()

    def delete(self, category: Category) -> None:
        self.session.delete(category)
        self.session.commit()
