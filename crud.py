from fastapi import FastAPI, Path, HTTPException, status
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()

# 🗄️ Changed from List to Dict for "Permanent IDs"
database = {} 
id_counter = 0 

class User(BaseModel):
    name: str = Field(..., min_length=3)
    age: int = Field(..., ge=18)

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create(user: User):
    global id_counter
    user_dict = user.model_dump()
    
    # Store with a permanent key
    database[id_counter] = user_dict
    id_counter += 1
    
    return {"id": id_counter - 1, "data": user_dict}

@app.get("/users/{u_id}")
async def read(u_id: Annotated[int, Path(ge=0)]):
    if u_id not in database:
        raise HTTPException(status_code=404, detail="User not found")
    return database[u_id]

@app.delete("/users/{u_id}")
async def delete(u_id: int):
    if u_id not in database:
        raise HTTPException(status_code=404)
    # Removing from dict doesn't change other keys!
    return database.pop(u_id)