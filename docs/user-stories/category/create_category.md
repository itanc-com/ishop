# User Story: Create Category

**As an** admin user
**I want** to create a new category with a name and optional parent category
**So that** I can organize products into logical groups

## Acceptance Criteria
- [x] Admin can submit a category name and optional parent ID
- [x] System validates input and checks for duplicate category names
- [x] On success, category is created and returned
- [ ] Error is returned if category already exists

## Notes
- Category creation uses a dedicated endpoint and usecase
- Parent-child relationships are supported
- Duplicate category names are not allowed

## Related Links
- [List Category](list_category.md)
- [Get Category](get_category.md)
