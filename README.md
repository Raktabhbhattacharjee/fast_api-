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

**Next Up: Day 2 - Query Parameters (Filtering data), so yea.**