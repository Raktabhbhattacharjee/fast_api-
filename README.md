# 🚀 30 Days of FastAPI: Engineering Log

This repository documents my transition from **Java/C++** to **FastAPI**. My goal is to master modern API development by replacing manual "if-else" boilerplate with declarative framework guards.

---

## 📅 Day 1: The "No-Boilerplate" Foundation
**Date:** Jan 6, 2026 | **Status:** Complete ✅

Today was about setting up the environment and understanding how FastAPI handles "pre-flight" logic automatically.

* **App Lifecycle:** `app = FastAPI()` is the central registry.
* **Decorators:** Used as Higher-Order Functions to map network routes to Python logic.
* **The Enum Shift:** Implemented `Enum` classes for strict validation. If an input is invalid, FastAPI blocks it with a `422 Unprocessable Entity` error before the function even runs.

---

## 📅 Day 2: Manual Logic & Model Dumping
**Date:** Jan 7, 2026 | **Status:** Complete ✅

Explored the communication layer between the URL and the server.

* **Parameter Scope:** Identified the difference between **Path** (Structural/Mandatory) and **Query** (Supplemental/Optional).
* **Data Preparation:** Used `.model_dump()` to bridge the gap between Pydantic models and Python dictionaries for future Pandas integration.
* **The Friction:** Realized that writing manual `if-else` checks to sanitize data is a "Java-style" habit that FastAPI can automate.

---

## 📅 Day 3: Parameter Mastery (The "Guard" Shift)
**Date:** Jan 8, 2026 | **Status:** Complete ✅

**The "Aha!" moment.** I moved manual data-cleaning logic directly into the function parameters using `Annotated`, `Query`, and `Path`.

### 🛡️ The Triple Guard System
I replaced manual checks with **Declarative Guards**:
1.  **Metadata:** `alias`, `title`, and `description` for auto-generated documentation.
2.  **String Stencils:** `min_length` and `pattern` (Regex) to ensure data purity.
3.  **Numeric Bounds:** `ge`, `le`, `gt`, and `lt` for strict integer and float safety.



### 💻 Master Boilerplate
```python
from typing import Annotated
from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    # PATH GUARD: Mandatory positive integer
    item_id: Annotated[int, Path(title="Item ID", ge=1, le=1000)],

    # QUERY GUARD: Regex-validated search string
    q: Annotated[str | None, Query(min_length=3, pattern="^[a-zA-Z\s]+$")] = None, 

    # NUMERIC GUARD: Float strictly greater than 0
    size: Annotated[float, Query(gt=0, lt=10.5)] = 5.5
):
    # Logic only executes if the guards pass. Data is 100% valid here.
    return {"item_id": item_id, "active_filters": q, "page_size": size}