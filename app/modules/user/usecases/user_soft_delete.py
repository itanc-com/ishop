# Implement the soft delete logic for a user.
# The function should:
# 1. Retrieve the user by ID using the repository.
# 2. If the user exists, set their status to UserStatus.DELETE.
# 3. Save the updated user back to the database (using repository update method).
# 4. If the user does not exist, raise an appropriate exception.


class UserSoftDelete:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def execute(self, user_id: int) -> None:
        # TODO: Complete the soft delete logic as described above
        pass
