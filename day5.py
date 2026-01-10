from typing import Annotated
from fastapi import FastAPI, Path, Body, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# 🗄️ MOCK DB: Our stateful list
database = [
    {"username": "rishi_dev", "age": 25}
]

# MODEL: Self-validating + Self-documenting
class UserProfile(BaseModel):
    username: str = Field(..., min_length=3, description="Username handle")
    age: int = Field(..., ge=18, description="User must be 18+")

    # NEW: This populates the 'Try it out' box in Swagger
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

#  the post logic 
@app.post("/users/", status_code=201)
async def create_user(user: UserProfile):
    # Convert Pydantic model to Dict
    user_dict = user.model_dump()
    
    # "Save" to our list
    database.append(user_dict)
    
    # Return the index as the ID (Common for list-based DBs)
    return {"id": len(database) - 1, "user": user_dict}

#  the get logic 
@app.get("/users/{user_id}")
async def get_user(user_id: Annotated[int, Path(ge=0)]):
    # Bounds check (The "C++ Safety" check)
    if user_id >= len(database):
        raise HTTPException(status_code=404, detail="User not found in memory")
    
    return database[user_id]