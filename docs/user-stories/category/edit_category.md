# User Story: Edit Category

**As an** admin user
**I want** to update the name or parent of an existing category
**So that** I can keep category information accurate and organized

## Acceptance Criteria
- [ ] Admin can update category name and/or parent ID
- [ ] System validates input and checks for conflicts
- [ ] On success, updated category is returned
- [ ] Error is returned if category does not exist or update fails

## Notes
- Editing uses a dedicated endpoint and usecase
- Parent-child relationships can be changed

## Related Links
- [Get Category](get_category.md)
- [Delete Category](delete_category.md)
