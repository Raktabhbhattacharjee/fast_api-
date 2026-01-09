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

---

## 📅 Day 4: Deep Modeling & Body Guards
**Date:** Jan 9, 2026 | **Status:** Complete ✅

Today I moved beyond URL parameters and mastered **Nested Data Modeling**. I replaced complex manual validation with self-guarding Pydantic classes.



### 🛡️ The Mastery Shift
* **Self-Guarding DTOs:** Used `Field()` inside classes for internal validation. This replaces the need for manual `if` statements inside the function.
* **Pre-Execution Rejection:** Confirmed that FastAPI kills requests with a `422` error (e.g., age < 18 or ID < 1) before the function body ever executes.
* **Hybrid Requests:** Created an endpoint that simultaneously guards the URL Path, the Query string, and a Nested JSON Body.

### 💻 Master Boilerplate (Day 4 Integrated)
```python
from typing import Annotated
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel, Field

app = FastAPI()

# MOCK DATABASE: Ready for Day 5 CRUD
database = []

# MODEL: Replaces Java-style manual validation logic
class UserProfile(BaseModel):
    username: str = Field(..., min_length=3, description="Must be 3+ chars")
    age: int = Field(..., ge=18, description="Adults only")

@app.put("/update-profile/{user_id}")
async def update_user(
    # PATH GUARD: URL must have positive integer
    user_id: Annotated[int, Path(ge=1)],               
    
    # BODY MODEL GUARD: Validates JSON against UserProfile class
    user_data: UserProfile,                            
    
    # SINGULAR BODY GUARD: Extra validated key in the JSON
    importance: Annotated[int, Body(gt=0, le=10)],     
    
    # QUERY GUARD: Optional URL flag (?confirm=true)
    confirm: bool = Query(False)                       
):
    # Logic only executes if all Guards pass!
    return {
        "user_id": user_id,
        "profile": user_data,
        "priority": importance,
        "is_confirmed": confirm,
        "status": "Validated & Ready for DB"
    }