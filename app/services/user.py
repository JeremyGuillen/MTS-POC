from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def list_users(self):
        return self.repository.list_all()

    def get_user(self, user_id: str):
        user = self.repository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        return user

    def create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str | None = None,
        role: str = "user",
        status: str = "active",
    ):
        existing_user = self.repository.get_by_email(email)

        if existing_user:
            raise ValueError("A user with this email already exists")

        return self.repository.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            role=role,
            status=status,
        )

    def update_user(self, user_id: str, data: dict):
        if "email" in data and data["email"]:
            existing_user = self.repository.get_by_email(data["email"])

            if existing_user and str(existing_user.id) != user_id:
                raise ValueError("A user with this email already exists")

        user = self.repository.update(user_id=user_id, data=data)

        if not user:
            raise ValueError("User not found")

        return user

    def delete_user(self, user_id: str):
        deleted = self.repository.delete(user_id)

        if not deleted:
            raise ValueError("User not found")

        return {"message": "User deleted successfully"}