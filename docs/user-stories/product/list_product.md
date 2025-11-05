# User Story: List All Products

**As a** system administrator or merchant
**I want** to retrieve a list of products, optionally filtered by category and paginated
**So that** I can view or manage multiple products efficiently

## Acceptance Criteria
- [x] The system supports optional filtering by `category_id`
- [x] Pagination parameters `page` and `per_page` control the returned product range
- [x] The use case retrieves products via the repository’s `list_all` method
- [x] If products exist, a list of `ProductRead` objects is returned
- [x] If no products are found, an `EntityNotFoundException` is raised with a clear message
- [ ] If a database error occurs, a `DatabaseOperationException` is raised with detailed context
- [ ] Endpoint (E2E) test verifies correct pagination, filtering, and response structure

## Notes
- Depends on `ProductRepositoryInterface` for data access
- Handles:
  - `EntityNotFoundException` → raised when no products are found for the given query
  - `DatabaseOperationException` → raised when a database or query operation fails
- Returns a list of validated `ProductRead` objects
- Pagination is controlled by parameters `page` (default 1) and `per_page` (default 10)

## Related Links
- [Create Product](create_product.md)
- [Get Product by ID](get_product.md)
- [Update Product](edit_product.md)
- [Delete Product](delete_product.md)
- [Check Product SKU Exists](product_sku_exists.md)

---

## 🧪 Test Scenarios

### ✅ Successful Listing
**Given** existing products in the database
**When** `ProductListAll.execute()` is called with default pagination
**Then** a list of `ProductRead` objects is returned

**Expected:**
- Response includes up to `per_page` items
- Each item matches the expected product schema
- HTTP response code (in API layer): `200 OK`

---

### ⚙️ Filter by Category
**Given** products belonging to multiple categories
**When** `ProductListAll.execute()` is called with a specific `category_id`
**Then** only products belonging to that category are returned

**Expected:**
- Response includes only filtered items
- Pagination and limit rules still apply

---

### ⚠️ No Products Found
**Given** an empty database or no products in the selected category
**When** `ProductListAll.execute()` is called
**Then** an `EntityNotFoundException` is raised

**Expected:**
- Exception message: `"No products found"`
- Response should use HTTP code `404 Not Found` in the API layer

---

### ❌ Database Error
**Given** a database connection failure or query issue
**When** `ProductListAll.execute()` is called
**Then** a `DatabaseOperationException` is raised

**Expected:**
- Exception includes operation `"select"`
- Error message describes the database failure
- No partial or invalid data is returned

---

## 🧭 Test Coverage Checklist
- [ ] E2E test for successful product listing with pagination
- [ ] E2E test for category-based filtering
- [ ] E2E test for empty result set (`EntityNotFoundException`)
- [ ] E2E test for `DatabaseOperationException` handling
- [ ] Validation of response structure and list schema (`ProductRead`)
