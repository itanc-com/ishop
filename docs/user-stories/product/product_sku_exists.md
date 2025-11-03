# User Story 1033: Check Product SKU Exists

**As a** system or service component
**I want** to verify whether a product with a specific SKU already exists
**So that** I can prevent duplicate product creation and maintain SKU uniqueness

## Acceptance Criteria
- [x] The use case accepts a SKU string as input
- [x] The repository method `exists_by_field("sku", sku)` is called to check existence
- [x] Returns `True` if a product with the given SKU exists, otherwise `False`
- [x] Raises `DatabaseOperationException` if any repository or database error occurs
- [ ] Unit test confirms correct results for existing and non-existing SKUs

## Notes
- This use case is intended for **internal validation** within other product operations (e.g., `ProductCreate`)
- It does **not** expose any API endpoint
- Depends on `ProductRepositoryInterface` for the data access layer
- Handles:
  - `DatabaseOperationException` → raised when the repository query fails
- No data mutation or transformation happens here; the logic is read-only

## Related Links
- [Create Product](create_product.md)
- [Get Product by ID](get_product.md)
- [Update Product](edit_product.md)
- [Delete Product](delete_product.md)
- [List All Products](list_product.md)

---

## 🧪 Test Scenarios

### ✅ SKU Exists
**Given** a product with SKU `ABC123` exists in the database
**When** `ProductSkuExists.execute("ABC123")` is called
**Then** the method returns `True`

---

### ⚙️ SKU Does Not Exist
**Given** no product with SKU `XYZ999` exists in the repository
**When** `ProductSkuExists.execute("XYZ999")` is called
**Then** the method returns `False`

---

### ❌ Repository or Database Error
**Given** the repository layer raises an exception (e.g., connection or query failure)
**When** `ProductSkuExists.execute("ANY_SKU")` is called
**Then** a `DatabaseOperationException` is raised
**And** the exception data contains the SKU value used in the query

---

## 🧭 Test Coverage Checklist
- [ ] Unit test for existing SKU → returns `True`
- [ ] Unit test for non-existing SKU → returns `False`
- [ ] Unit test for `DatabaseOperationException` on repository failure
