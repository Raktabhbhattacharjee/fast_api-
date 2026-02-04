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
| **07** | **Real Persistence** | ✅ | **SQLModel & SQLite Integration** |

---

## 📅 Day 5 & 6: The "Production-Ready" Leap
**Status:** Complete ✅

I successfully moved from basic validation to building a **Complete Stateful CRUD System**. I realized that for an API to be robust, I must handle state changes (Deletes/Updates) without breaking the data structure.

### 🛡️ The Mastery Shift
* **Permanent ID Strategy:** Moved from list indices to a Global ID counter. This prevents the "Index Shift" bug where deleting one user changes everyone else's ID.
* **Contract-First Docs:** Implemented `model_config` with `examples`. This officially replaced Postman in my workflow as the Swagger UI now serves as a live test suite.
* **Declarative Guards:** Mastered the use of `Annotated[int, Path(ge=0)]` to ensure the API never even processes negative or invalid IDs.

---

## 📅 Day 07: The Persistence Leap (SQLModel & SQLite)
**Date:** Feb 04, 2026 | **Status:** Complete ✅

Today I successfully replaced the "Fake Database" (Python Dictionary) with a **Physical SQL Database**. Coming from a C++/Java background, this felt like moving from a simple `HashMap` to a fully managed **Hibernate/JPA** layer.

### 🛡️ The Architectural Shift
* **From Memory to Disk:** Data now survives server restarts and crashes. Using `sqlite:///database.db` ensures the state is persistent.
* **Unified Modeling:** Implemented `SQLModel`. By setting `table=True`, a single class now acts as both a **Pydantic Validation Shield** and a **SQL Table Definition**.
* **Automatic Integrity:** Leveraged SQL **Primary Keys**. I no longer need a manual `id_counter`; the database engine handles unique ID generation and prevents collisions (Integrity Errors).



### 💻 The "Persistence" Code (Master Script)

```python
from typing import Annotated, List, Optional
from fastapi import FastAPI, HTTPException, Path, Depends, status
from sqlmodel import SQLModel, Field, create_engine, Session, select

# --- 1. DATABASE ENGINE SETUP ---
sqlite_url = "sqlite:///database.db"
# connect_args ensures compatibility with FastAPI's async multi-threading
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

def get_session():
    """Dependency Provider for Database Transactions"""
    with Session(engine) as session:
        yield session

app = FastAPI(title="Day 7: SQL Persistence")

# --- 2. THE UNIFIED SCHEMA ---
class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) 
    username: str = Field(index=True, min_length=3)
    age: int = Field(ge=18)

@app.on_event("startup")
def on_startup():
    # Automatically creates 'database.db' and the UserProfile table
    SQLModel.metadata.create_all(engine)

# --- 3. PERSISTENT CRUD LOGIC ---

@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=UserProfile)
async def create_user(user: UserProfile, session: Session = Depends(get_session)):
    # SQL Transaction: Add -> Commit -> Refresh (to get the new ID)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/", response_model=List[UserProfile])
async def get_all_users(session: Session = Depends(get_session)):
    return session.exec(select(UserProfile)).all()

@app.get("/users/{user_id}", response_model