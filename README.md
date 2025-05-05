# iShop – Online Shop API

A simple and lightweight eCommerce API built with FastAPI to manage online sales and inventory.

---

## 🚀 Features

- Product listing and management  
- Cart and order handling  
- Simple and extensible architecture  
- Suitable for small-scale eCommerce projects  

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