# app/repositories/mold_repository.py
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.mold import Mold


class MoldRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[Mold]:
        return self.db.query(Mold).order_by(Mold.id).all()

    def create(self, name: str, catalog: str | None = None) -> Mold:
        mold = Mold(catalog=catalog, entry_date=datetime.now())

        self.db.add(mold)
        self.db.commit()
        self.db.refresh(mold)

        return mold
