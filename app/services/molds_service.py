from datetime import datetime
from app.repositories.mold_repository import MoldRepository


class MoldService:
    def __init__(self, repository: MoldRepository):
        self.repository = repository

    def list_molds(self):
        return self.repository.list_all()

    def create_mold(self, name: str, entry_date: datetime):
        return self.repository.create(name=name, entry_date=entry_date)
