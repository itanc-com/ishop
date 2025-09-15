# User Story: Soft Delete User (Status Change)

**As an** admin user
**I want** to mark a user as deleted by updating their status, without removing their record from the database
**So that** I can retain user data for audit or recovery purposes while preventing access

## Acceptance Criteria
- [x] Admin can set a user's status to DELETE
- [x] System prevents deleted users from logging in or accessing features
- [ ] User data remains in the database for future reference
- [ ] System confirms successful status change

## Notes
- This is a soft delete: the user record is not removed, only the status is updated
- Useful for compliance, audit, or recovery scenarios
- UserStatus enum includes DELETE for this purpose

## Related Links
- [Delete User with Cascade](delete_user.md)
- [Get User](get_user.md)
