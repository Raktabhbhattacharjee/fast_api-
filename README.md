# 🚀 30 Days of FastAPI: Engineering Log

This repository documents my transition from **Java/C++** to **FastAPI**. My goal is to master modern API development by replacing manual "if-else" boilerplate with declarative framework guards.

---

## 📅 Progress Tracker

| Day | Focus | Status | Key Concept |
| :--- | :--- | :--- | :--- |
| **01** | The Foundation | ✅ | Decorators & Type Hinting |
| **02** | Data Prep | ✅ | `.model_dump()` Serialization |
| **03** | Parameter Guards | ✅ | `Annotated` for Path/Query security |
| **04** | Deep Modeling | ✅ | `Field()` level validation |
| **05/06** | **The CRUD Master** | ✅ | **Full State Management & Permanent IDs** |

---

## 📅 Day 5 & 6: The "Production-Ready" Leap
**Date:** Jan 14, 2026 | **Status:** Complete ✅

I have successfully moved from basic validation to building a **Complete Stateful CRUD System**. I realized that for an API to be robust, I must handle state changes (Deletes/Updates) without breaking the data structure.

### 🛡️ The Mastery Shift
* **Permanent ID Strategy:** Moved from list indices to a Global ID counter. This prevents the "Index Shift" bug where deleting one user changes everyone else's ID.
* **Contract-First Docs:** Implemented `model_config` with `examples`. This officially replaced Postman in my workflow as the Swagger UI now serves as a live test suite.
* **Declarative Guards:** Mastered the use of `Annotated[int, Path(ge=0)]` to ensure the API never even processes negative or invalid IDs.



### 💻 The Full "Master" Code (80+ Lines of Logic)

```python
from typing import Annotated
from fastapi import FastAPI, Path, Body, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

# 🗄️ STATEFUL DATABASE (Using Dict for Permanent ID Mapping)
database = {} 
id_counter = 0

# --- MODEL DEFINITION ---
class UserProfile(BaseModel):
    username: str = Field(..., min_length=3, description="Username handle")
    age: int = Field(..., ge=18, description="User must be 18+")

    # Self-Documenting Contract for Swagger UI
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "fastapi_pro",
                    "age": 30
                }
            ]
        }
    }

# --- 1. CREATE (POST) ---
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserProfile):
    global id_counter
    
    # Bridge: Object -> Storage Format
    user_dict = user.model_dump()
    
    # Assign permanent ID and store
    database[id_counter] = user_dict
    current_id = id_counter
    id_counter += 1
    
    return {"id": current_id, "user": user_dict}

# --- 2. READ ALL (GET) ---
@app.get("/users/")
async def get_all_users():
    return database

# --- 3. READ ONE (GET) ---
@app.get("/users/{user_id}")
async def get_user(user_id: Annotated[int, Path(ge=0)]):
    if user_id not in database:
        raise HTTPException(
            status_code=404, 
            detail=f"User with ID {user_id} not found in memory"
        )
    return database[user_id]

# --- 4. UPDATE (PUT) ---
@app.put("/users/{user_id}")
async def update_user(
    user_id: Annotated[int, Path(ge=0)], 
    updated_user: UserProfile
):
    if user_id not in database:
        raise HTTPException(status_code=404, detail="Cannot update - ID does not exist")
    
    # Overwrite existing record with new validated data
    database[user_id] = updated_user.model_dump()
    return {"message": "Update Successful", "data": database[user_id]}

# --- 5. DELETE (DELETE) ---
@app.delete("/users/{user_id}")
async def delete_user(user_id: Annotated[int, Path(ge=0)]):
    if user_id not in database:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Remove from dictionary (Does not shift other IDs)
    deleted_item = database.pop(user_id)
    return {"status": "Deleted", "last_record": deleted_item}
    ---

## 📅 Day 07: Mega Revision (The Mastery Leap)
**Date:** Jan 18, 2026 | **Status:** Complete ✅

Successfully consolidated 7 days of learning into a single **Mega Revision** script. This marks the transition from basic syntax to understanding the full lifecycle of a RESTful API.

### 🛡️ Core Concepts Mastered:
* **Pydantic Guards:** Moving logic out of the function body and into the Model (declarative programming).
* **State Integrity:** Using a global ID counter to ensure IDs never overlap, even if items are deleted.
* **Response Codes:** Using `201` for creation and `204` for deletion (standard API engineering).
* **Path Decorators:** Using `Annotated` for input sanitization (preventing negative IDs).

### 🚀 Next Step:
Moving from List-based memory to **Real Persistence** using SQLModel and SQLite.