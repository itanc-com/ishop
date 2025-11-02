# User Story: Delete User with Cascade

**As an** admin user
**I want** to delete a user and all related data (orders, cart, etc.) automatically
**So that** I can ensure data integrity and remove all traces of the user from the system

## Acceptance Criteria
- [x] Admin can delete a user by ID
- [x] System deletes the user and all related records (orders, cart, etc.) in a single operation
- [ ] Error is returned if user does not exist
- [ ] System confirms successful deletion of user and related data

## Notes
- Deletion uses a dedicated endpoint and usecase
- Cascade delete ensures no orphaned records remain
- Related data includes orders, cart items, and other user-linked entities

## Related Links
- [Get User](get_user.md)
- [Edit User](edit_user.md)
