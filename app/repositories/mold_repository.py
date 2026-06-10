from sqlalchemy.orm import Session
from datetime import datetime

from app.models.mold import Mold


class MoldRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[Mold]:
        return self.db.query(Mold).order_by(Mold.name.asc()).all()

    def create(self, name: str, entry_date: datetime) -> Mold:
        mold = Mold(name=name, entry_date=entry_date)

        self.db.add(mold)
        self.db.commit()
        self.db.refresh(mold)

        return mold
