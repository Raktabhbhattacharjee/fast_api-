from typing import Annotated
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel, Field

app = FastAPI()

# --- 1. THE DATA BLUEPRINT (THE SCHEMA) ---
class User(BaseModel):
    # 'Field' replaces manual 'if len(name) < 3'
    username: str = Field(..., min_length=3, description="The login name")
    # 'Field' replaces manual 'if age < 18'
    age: int = Field(..., ge=18, message="Must be an adult")

# --- 2. THE MULTI-GUARD ENDPOINT ---
@app.put("/update-profile/{user_id}")
async def update_user(
    # GUARD 1: URL Path (Yesterday's logic)
    user_id: Annotated[int, Path(title="The ID to update", ge=1)],
    
    # GUARD 2: The Body Object (Today's logic)
    # FastAPI sees 'User' class, so it looks for a JSON body
    user_data: User,
    
    # GUARD 3: The Singular Body Value (Level 3 logic)
    # Forces 'importance' into the JSON instead of the URL
    importance: Annotated[int, Body(gt=0)],
    
    # GUARD 4: The Query (Yesterday's logic)
    confirm: Annotated[bool, Query()] = False
):
    # 3. THE BUSINESS LOGIC (The 'Do-er')
    return {
        "user_id": user_id,
        "new_data": user_data,
        "importance": importance,
        "confirmed": confirm
    }