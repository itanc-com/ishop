## 🛠️ Development Guidelines

This project follows standard Python conventions to ensure consistency and maintainability.

### 📛 Naming Convention (PEP 8)

We follow the [PEP 8](https://peps.python.org/pep-0008/) naming conventions for all Python code. Below is a quick reference:

| Item                   | Naming Style       | Example                        |
|------------------------|--------------------|--------------------------------|
| **Modules / Files**    | `snake_case.py`    | `user_repository.py`           |
| **Packages / Folders** | `snake_case/`      | `payment_gateways/`            |
| **Classes**            | `CamelCase`        | `UserRepository`, `OrderService` |
| **Interfaces / ABCs**  | `CamelCase`        | `UserRepositoryInterface`, `AbstractPaymentGateway` |
| **Functions / Methods**| `snake_case()`     | `get_by_email()`, `process_order()` |
| **Variables**          | `snake_case`       | `user_data`, `order_id`        |
| **Constants**          | `ALL_CAPS`         | `JWT_SECRET_KEY`, `MAX_RETRIES` |
| **Type Hints**         | Use clear types    | `email: str`, `items: list[str]` |

> 🧠 **Note**: Avoid using Java-style prefixes like `IUserRepository`. Prefer descriptive names such as `UserRepositoryInterface`.

---

For consistent code formatting and linting, we recommend using:

- [**Ruff**](https://github.com/charliermarsh/ruff) – for linting

You can configure these in your `pyproject.toml` or setup files.

---


# 📦 Import Guidelines

This project follows a consistent import strategy based on [PEP 8](https://peps.python.org/pep-0008/) to ensure readability, testability, and maintainability.

---

## ✅ General Rules

| Type of Import             | Style           | When to Use                                | Example                                                  |
|---------------------------|------------------|---------------------------------------------|-----------------------------------------------------------|
| **Standard Library**       | Absolute         | Always                                      | `import os`, `from datetime import datetime`             |
| **Third-party packages**   | Absolute         | Always                                      | `from sqlalchemy.orm import Session`                     |
| **App-wide modules**       | Absolute         | From other modules in your app             | `from app.utils.security.password_context import PasswordContext` |
| **Same-package modules**   | Relative         | For importing between files in same folder | `from .repository_interface import UserRepositoryInterface` |

---

## 📍 Examples

### ✅ Absolute Import (App-level)
Use for anything outside the current folder/module.

```python
# Correct usage
from app.utils.security.password_context import PasswordContext
from app.common.exceptions.app_exceptions import DuplicateEntryException
```
