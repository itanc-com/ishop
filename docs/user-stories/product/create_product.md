# User Story: Create a New Product

**As a** system administrator or merchant
**I want** to create a new product by providing all required product details
**So that** the product is added to the catalog and available for sale or management

## Acceptance Criteria
- [x] Product creation validates all required fields (e.g., name, SKU, price, etc.)
- [x] SKU uniqueness is checked before saving; duplicates raise a `DuplicateEntryException`
- [x] A successful creation returns a `ProductRead` object with the new product data
- [x] If a database error occurs, a `DatabaseOperationException` is raised
- [x] The use case integrates with the `ProductRepositoryInterface` for persistence
- [x] Input is validated according to the `ProductInCreate` schema
- [ ] Comprehensive tests are written to verify all success and failure scenarios

## Notes
- Depends on `ProductRepositoryInterface` and `ProductSkuExists` use cases
- Handles `DuplicateEntryException` and `DatabaseOperationException`
- Response format is standardized via `ProductRead` schema

## Related Links
- [Get Product by ID](get_product.md)
- [Update Product](edit_product.md)
- [Delete Product](delete_product.md)
- [List All Products](list_product.md)
- [Check Product SKU Exists](product_sku_exists.md)
