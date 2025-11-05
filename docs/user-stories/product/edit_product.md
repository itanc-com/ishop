# User Story: Edit an Existing Product

**As a** system administrator or merchant
**I want** to update an existing product’s details
**So that** I can correct information or modify product attributes such as price, name, or stock

## Acceptance Criteria
- [x] The system accepts a valid `product_id` and a `ProductUpdate` payload
- [x] The repository updates the product record with the provided fields
- [x] If the update is successful, the use case returns a `ProductRead` object containing updated data
- [x] If the product does not exist, an `EntityNotFoundException` is raised with a clear message
- [x] If a database error occurs during update, a `DatabaseOperationException` is raised with error details
- [x] All required fields in `ProductUpdate` are validated before execution
- [ ] Comprehensive unit and integration tests are implemented to cover all success and failure paths

## Notes
- Depends on `ProductRepositoryInterface` for persistence operations
- Handles:
  - `EntityNotFoundException` → when the product ID does not exist
  - `DatabaseOperationException` → for update failures at the repository or database level
- Returns a `ProductRead` schema object that reflects the updated product
- (Minor issue to fix): The `DatabaseOperationException` currently uses `"delete"` as operation name; should be `"update"`

## Related Links
- [Create Product](create_product.md)
- [Get Product by ID](get_product.md)
- [Delete Product](delete_product.md)
- [List All Products](list_product.md)
- [Check Product SKU Exists](product_sku_exists.md)


---

## 🧪 Test Scenarios

### ✅ Successful Update
**Given** a valid `product_id` and a valid `ProductUpdate` object
**When** `ProductEdit.execute()` is called
**Then** the product record is updated and returned as a `ProductRead` object

**Expected:**
- Updated fields reflect new values
- No exceptions are raised
- HTTP response (in API layer) should return status code `200 OK`

---

### ⚠️ Product Not Found
**Given** a `product_id` that does not exist in the repository
**When** `ProductEdit.execute()` is called
**Then** an `EntityNotFoundException` is raised

**Expected:**
- Exception message: `"Product not found"`
- No database changes occur

---

### ❌ Database Error
**Given** a valid `product_id` and update data
**When** a database failure occurs during update
**Then** a `DatabaseOperationException` is raised

**Expected:**
- Exception includes operation `"update"`
- Error message describes the database error cause
- The original data remains unchanged

---

## 🧭 Test Coverage Checklist
- [ ] Unit test for successful update
- [ ] Unit test for `EntityNotFoundException` (product not found)
- [ ] Unit test for `DatabaseOperationException` (database failure)
- [ ] Validation test ensuring input matches `ProductUpdate` schema
- [ ] Integration test confirming returned `ProductRead` structure
- [ ] Ensure HTTP 200 is returned from API layer on success
