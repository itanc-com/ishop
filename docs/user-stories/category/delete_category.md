# User Story: Delete Category

**As an** admin user
**I want** to delete a category by its ID
**So that** I can remove obsolete or incorrect categories

## Acceptance Criteria
- [x] Admin can delete a category by ID
- [x] System checks if category exists before deleting
- [ ] On success, category is removed from the system
- [ ] Error is returned if category does not exist

## Notes
- Deletion uses a dedicated endpoint and usecase
- Related products or subcategories may need to be handled

## Related Links
- [List Category](list_category.md)
- [Edit Category](edit_category.md)
