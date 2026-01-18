from typing import Annotated, List, Optional
from fastapi import FastAPI, Path, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Day 7: Mega Revision CRUD",
    description="Consolidating Java/C++ logic into Pythonic FastAPI code."
)

# --- 1. THE DATA CONTRACT ---
class UserProfile(BaseModel):
    # Strict validation: like Java's Bean Validation (@Min, @Size)
    username: str = Field(..., min_length=3, max_length=20, description="Username handle")
    age: int = Field(..., ge=18, le=120, description="Must be 18 or older")
    email: Optional[str] = Field(None, pattern=r"^\S+@\S+\.\S+$", description="Valid email format")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "fastapi_pro",
                    "age": 25,
                    "email": "dev@example.com"
                }
            ]
        }
    }

# --- 2. IN-MEMORY STATE ---
database: List[dict] = []
id_counter: int = 1

# --- 3. CRUD LOGIC ---

# CREATE
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserProfile):
    global id_counter
    user_dict = user.model_dump()
    user_dict["id"] = id_counter
    database.append(user_dict)
    id_counter += 1
    return user_dict

# READ ALL
@app.get("/users/")
async def get_all_users():
    return database

# READ ONE
@app.get("/users/{user_id}")
async def get_user(user_id: Annotated[int, Path(ge=1)]):
    for user in database:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# UPDATE
@app.put("/users/{user_id}")
async def update_user(user_id: Annotated[int, Path(ge=1)], updated_data: UserProfile):
    for index, user in enumerate(database):
        if user["id"] == user_id:
            updated_user = updated_data.model_dump()
            updated_user["id"] = user_id
            database[index] = updated_user
            return {"status": "Updated", "user": updated_user}
    raise HTTPException(status_code=404, detail="User not found")

# DELETE
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: Annotated[int, Path(ge=1)]):
    for index, user in enumerate(database):
        if user["id"] == user_id:
            database.pop(index)
            return
    raise HTTPException(status_code=404, detail="User not found")