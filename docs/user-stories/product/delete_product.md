# User Story: Delete an Existing Product

**As a** system administrator or merchant
**I want** to delete an existing product by its unique ID
**So that** it can be removed from the product catalog when it is no longer needed or available

## Acceptance Criteria
- [x] The system receives a valid `product_id` for deletion
- [x] If the product exists, it is deleted successfully from the repository
- [x] Upon successful deletion, the use case returns a `ProductRead` object representing the deleted product
- [x] If the product does not exist, an `EntityNotFoundException` is raised with a meaningful message
- [x] If a database error occurs during deletion, a `DatabaseOperationException` is raised with error context
- [ ] HTTP response for successful deletion must return status code `200`
- [ ] Comprehensive tests are written to verify all success and failure scenarios

## Notes
- Depends on `ProductRepositoryInterface` for data persistence
- Handles:
  - `DatabaseOperationException` → raised for database-level issues
  - `EntityNotFoundException` → raised when the specified product ID does not exist
- Returns a validated `ProductRead` schema of the deleted product

## Related Links
- [Create Product](create_product.md)
- [Get Product by ID](get_product.md)
- [Update Product](edit_product.md)
- [List All Products](list_product.md)
- [Check Product SKU Exists](product_sku_exists.md)
