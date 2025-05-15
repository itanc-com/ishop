# iShop – E-commerce API with FastAPI Framework

## A simple and lightweight e-commerce API built with FastAPI for managing online sales and inventory.

---

## 🚀 Features

- Product listing and management  
- Cart and order handling  
- Simple and extensible architecture  
- Suitable for small-scale eCommerce projects  

[🗂️ View iShop Database Diagram on dbdiagram.io](https://dbdiagram.io/d/iShop-68252d1f5b2fc4582fa8803d)

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/itanc-com/ishop.git

cd ishop
```
### 2. Create and Activate Virtual Environment

```
uv venv

source .venv/bin/activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

## Setup Environment 


## Running the App
You can run the app in development or production mode.

### ✅ Option 1: Run with run.py

```
python3 run.py
```
### ✅ Option 2: Use FastAPI CLI

#### Development Mode 
```
uv run fastapi dev
```

#### Production Mode

```
fastapi run
```

#### Run on custom port 

```
uv run fastapi dev --host 0.0.0.0 --port 5001
```

### 📋 Requirements

- Python 3.11+
- FastAPI
- uv (optional, for faster workflows)

### 🛠️ Development Note

If you want to add a feature to the project and need to install new packages, follow these steps:

#### ➕ Add Dependencies with `uv`

Use `uv pip install` instead of regular `pip install`. This ensures that packages are installed in a reproducible and isolated environment managed by `uv`.

```bash
uv pip install <package-name>
```

For example :

```
uv pip install httpx
```

This automatically updates your virtual environment and makes the package available in the project.



#### 📦 Update requirements.txt

After installing or upgrading packages, freeze the current environment into requirements.txt

```
uv pip freeze > requirements.txt
```


### ENV File Parameters
This file contains configuration values used by the application.
It's typically used to separate environment-specific settings from the application code.

**filename : app/.env**

```
ENVIRONMENT='DEV' # environment variable permitted: 'DEV', 'PROD', 'TEST' 
DATABASE_URI="sqlite:///./app/db/db.sqlite3"
JWT_ISSUER_SERVER="localhost:8000"
JWT_SECRET_KEY="your_secure_key"
```