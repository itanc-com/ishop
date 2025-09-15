from app.modules.user.repository_interface import UserRepositoryInterface


# Implement the hard delete logic for a user.
# The function should:
# 1. Remove the user from the database by ID using the repository.
# 2. If the user does not exist, raise an appropriate exception.
# This is a true delete: the user record is permanently removed from the database.
class UserDelete:
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def execute(self, user_id: int) -> None:
        # TODO: Complete the hard delete logic as described above
        pass
