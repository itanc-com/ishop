# User Story: Get Product by ID

**As a** system administrator or merchant
**I want** to retrieve a product’s details using its unique ID
**So that** I can view the product information for management or display purposes

## Acceptance Criteria
- [x] The system accepts a valid `product_id` as input
- [x] The use case retrieves the corresponding product from the repository
- [x] If the product exists, it returns a `ProductRead` object with all product details
- [x] If the product does not exist, an `EntityNotFoundException` is raised with a clear message
- [x] If a database or query error occurs, a `DatabaseOperationException` is raised with error details
- [ ] Comprehensive unit and integration tests are implemented to verify all behaviors

## Notes
- Depends on `ProductRepositoryInterface` for data access
- Handles:
  - `EntityNotFoundException` → raised when the product ID is not found
  - `DatabaseOperationException` → raised when a database query fails
- Returns a validated `ProductRead` schema containing full product details
- Operation type in exception: `"select"`

## Related Links
- [Create Product](create_product.md)
- [Update Product](edit_product.md)
- [Delete Product](delete_product.md)
- [List All Products](list_product.md)
- [Check Product SKU Exists](product_sku_exists.md)

---

## 🧪 Test Scenarios

### ✅ Successful Retrieval
**Given** a valid `product_id` that exists in the repository
**When** `ProductGetById.execute()` is called
**Then** the product is retrieved successfully and returned as a `ProductRead` object

**Expected:**
- Returned data matches the stored product
- No exceptions are raised
- HTTP response (in API layer) should return status code `200 OK`

---

### ⚠️ Product Not Found
**Given** a `product_id` that does not exist in the database
**When** `ProductGetById.execute()` is called
**Then** an `EntityNotFoundException` is raised

**Expected:**
- Exception message: `"Product not found"`
- Response should contain appropriate HTTP error code (`404 Not Found`)

---

### ❌ Database Error
**Given** a valid `product_id`
**When** a database failure occurs during lookup
**Then** a `DatabaseOperationException` is raised

**Expected:**
- Exception includes operation `"select"`
- Error message provides details of the failure
- No partial or invalid data is returned

---

## 🧭 Test Coverage Checklist
- [ ] Unit test for successful retrieval of existing product
- [ ] Unit test for `EntityNotFoundException` when product does not exist
- [ ] Unit test for `DatabaseOperationException` when repository raises an error
- [ ] Validation test ensuring output conforms to `ProductRead` schema
- [ ] Integration test verifying correct API response (`200 OK` / `404 Not Found`)
