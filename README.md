# 🚀 30 Days of FastAPI

### Day 1: The "No-Boilerplate" & Validation Logic
**Date:** Jan 6, 2026  
**Status:** Complete ✅

Today was about setting up the environment and seeing how FastAPI handles the "guard" logic automatically so I don't have to write it manually, so yea.

### 🧠 My Learning Log
* **The App Object:** `app = FastAPI()` is the main instance. Everything connects here.
* **Decorators (@):** These are like inbuilt Higher Order Functions. I just tell it the path and the method (GET, POST, etc.), and it sits on top of my function logic, so yea.
* **Coroutines:** `async def` functions return a Coroutine object. It handles the asynchronous execution in the background.
* **Automatic JSON:** I can return a dict, list, or singular values like int or str. FastAPI converts it to JSON automatically, so yea.

### 🛠️ The "No Postman" Workflow
The interactive docs are the best part because I don't have to type anything manually to test.
* I just go to `/docs` and the UI is already built based on my code.
* It catches bugs (like wrong data types) before the code even runs my main function.
* It’s a full testing suite that documents itself, so yea.

### 🛡️ High-Level Validation vs. Manual Logic
I realized I don't need to write manual "if" checks to see if a value is valid anymore.

* **The Enum Shift:** I just use an **Enum Class**. I don't use shortcuts like `.value` manually just to check if a string exists in a list.
* **The Result:** If I input something wrong (like my name `raktabh`), FastAPI blocks it and sends a `detail` error immediately. It tells the user exactly what was expected (like `'gemini' or 'developer'`).
* **The Win:** The framework handles the "pre-flight" check so I only have to focus on the logic when the data is 100% correct, so yea.

---

### ✅ Day 1 Checklist
- [x] Initialized Git (Working tree clean).
- [x] Set up `.venv` (Environment isolation).
- [x] Created `app/main.py` with Path Parameters.
- [x] Used Enum classes for predefined dropdown values.
- [x] Verified auto-validation in `/docs`.

# 🚀 30 Days of FastAPI

### Day 2: The Logic of Parameters (Query & Path)
**Date:** Jan 7, 2026  
**Status:** Complete ✅

Today was about learning how to communicate with the API via the URL. I learned that FastAPI identifies data based on where I define it—either in the "Address" (Path) or the "Function" (Query), so yea.

### 🧠 My Learning Log
* **Path Parameters (`/items/{id}`):**
    * These live inside the decorator: `@app.get("/items/{item_id}")`.
    * They are mandatory. If the ID isn't in the URL, the route won't even trigger.
    * Use these for "Primary Keys" to identify a specific resource, so yea.

* **Query Parameters (`?limit=10`):**
    * These are **NOT** in the decorator; they only live in the function signature: `async def read(limit: int)`.
    * They are used for filtering, sorting, or searching through data.
    * FastAPI knows it's a Query Param automatically because it's missing from the decorator path.



### 🛠️ The "Safety" Logic (Defaults & Optionals)
I don't have to worry about the API crashing if a user misses a filter. I can bake the logic directly into the parameters:
* **Optional Values:** Using `str | None = None` makes a parameter optional. If the user doesn't send it, the code just skips it.
* **Smart Defaults:** Setting `limit: int = 10` ensures that even if the user is lazy, my logic still has a number to work with.
* **Type Guard:** If I expect an `int` and get a `string`, FastAPI blocks the request before it even hits my main logic, so yea.



### 🛡️ Mixing Parameters
The real "Main Logic" happens when you combine them. I can identify a user via **Path** and then filter their data via **Query**:
```python
@app.get("/users/{user_id}/items")
async def get_items(user_id: int, limit: int = 10, category: str | None = None):
    # Identifies WHO (Path) and WHAT/HOW MANY (Query)
    return {"user": user_id, "limit": limit, "cat": category}