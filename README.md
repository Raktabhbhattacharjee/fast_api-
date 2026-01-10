# 🚀 30 Days of FastAPI: Engineering Log

This repository documents my transition from **Java/C++** to **FastAPI**. My goal is to master modern API development by replacing manual "if-else" boilerplate with declarative framework guards.

---

## 📅 Day 1: The "No-Boilerplate" Foundation
**Date:** Jan 6, 2026 | **Status:** Complete ✅

* **App Lifecycle:** `app = FastAPI()` is the central registry.
* **Decorators:** Used as Higher-Order Functions to map network routes to Python logic.
* **The Enum Shift:** Implemented `Enum` classes for strict validation.

---

## 📅 Day 2: Manual Logic & Model Dumping
**Date:** Jan 7, 2026 | **Status:** Complete ✅

* **Parameter Scope:** Identified the difference between **Path** and **Query**.
* **Data Preparation:** Used `.model_dump()` to bridge the gap between Pydantic and Dictionaries.

---

## 📅 Day 3: Parameter Mastery (The "Guard" Shift)
**Date:** Jan 8, 2026 | **Status:** Complete ✅

**The "Aha!" moment.** I moved manual data-cleaning logic directly into the function parameters using `Annotated`, `Query`, and `Path`.

---

## 📅 Day 4: Deep Modeling & Body Guards
**Date:** Jan 9, 2026 | **Status:** Complete ✅

* **Self-Guarding DTOs:** Used `Field()` inside classes for internal validation.
* **Pre-Execution Rejection:** Confirmed that FastAPI kills requests with a `422` error before the function body executes.

---

## 📅 Day 5: The "Contract-First" Shift & State Management
**Date:** Jan 10, 2026 | **Status:** Complete ✅

Today marked a major milestone: building a functional **Stateful API** (Create, Read, Update) without following step-by-step tutorials.

### 🛡️ The Mastery Shift
* **Living Documentation:** Discovered `model_config`. This populates the Swagger UI with **Example Payloads**, creating a visual contract for the consumer.
* **Stateful Logic:** Implemented a mock database using Python lists. Learned to bridge the gap between Pydantic Objects and storage using `.model_dump()`.
* **Manual Exception Handling:** Applied the "C++ Safety" mindset by manually raising `HTTPException(status_code=404)` for index-out-of-bounds errors.
* **The Parser vs. The Guard:** Identified that a **422 Error** can be triggered by either a JSON syntax mistake (the parser) or a logic violation (Pydantic).

### 💻 Master Boilerplate (Day 5 Integrated CRUD)
```python
from typing import Annotated
from fastapi import FastAPI, Path, Body, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# MOCK DB: Persistence in RAM for the session
database = [{"username": "rishi_dev", "age": 25}]

class UserProfile(BaseModel):
    username: str = Field(..., min_length=3, description="Username handle")
    age: int = Field(..., ge=18, description="User must be 18+")

    model_config = {
        "json_schema_extra": {
            "examples": [{"username": "fastapi_pro", "age": 30}]
        }
    }

@app.post("/users/", status_code=201)
async def create_user(user: UserProfile):
    user_dict = user.model_dump()
    database.append(user_dict)
    return {"id": len(database) - 1, "user": user_dict}

@app.get("/users/{user_id}")
async def get_user(user_id: Annotated[int, Path(ge=0)]):
    if user_id >= len(database):
        raise HTTPException(status_code=404, detail="User not found in memory")
    return database[user_id]

@app.put("/users/{user_id}")
async def update_user(user_id: Annotated[int, Path(ge=0)], updated_user: UserProfile):
    if user_id >= len(database):
        raise HTTPException(status_code=404, detail="Cannot update - ID does not exist")
    database[user_id] = updated_user.model_dump()
    return {"message": "Update Successful", "data": database[user_id]}