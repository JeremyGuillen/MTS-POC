import uuid

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> list[User]:
        return self.db.query(User).order_by(User.first_name.asc(), User.last_name.asc()).all()

    def get_by_id(self, user_id: str) -> User | None:
        try:
            parsed_user_id = uuid.UUID(user_id)
        except ValueError:
            return None

        return self.db.query(User).filter(User.id == parsed_user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.email == email.lower().strip())
            .first()
        )

    def create(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str | None = None,
        role: str = "user",
        status: str = "active",
    ) -> User:
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email.lower().strip(),
            phone=phone,
            role=role,
            status=status,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def update(self, user_id: str, data: dict) -> User | None:
        user = self.get_by_id(user_id)

        if not user:
            return None

        if "email" in data and data["email"]:
            data["email"] = data["email"].lower().strip()

        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)

        return user

    def delete(self, user_id: str) -> bool:
        user = self.get_by_id(user_id)

        if not user:
            return False

        self.db.delete(user)
        self.db.commit()

        return True