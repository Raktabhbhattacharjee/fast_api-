from typing import Annotated
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel, Field

# --- INITIALIZATION ---
app = FastAPI()

# FAKE DATABASE: A simple list to store our validated objects for Day 5
database = []

# --- DAY 4: DATA MODELING (The Java 'DTO' replacement) ---
# This class acts as a 'Self-Guarding' object.
class UserProfile(BaseModel):
    # Rule: Username must be 3+ chars. Field replaces manual 'if' checks.
    username: str = Field(..., min_length=3, description="Username must be at least 3 characters")
    # Rule: Must be 18 or older.
    age: int = Field(..., ge=18, description="User must be an adult")

# --- DAY 3 RECAP: PARAMETER GUARDS ---
@app.get("/items/{item_id}")
async def read_items(
    # PATH GUARD: Structural/Mandatory ID between 1 and 1000
    item_id: Annotated[int, Path(title="Item ID", ge=1, le=1000)],
    # QUERY GUARD: Optional search string with Regex safety
    q: Annotated[str | None, Query(min_length=3, pattern="^[a-zA-Z\s]+$")] = None
):
    return {"item_id": item_id, "search_query": q}

# --- DAY 4 MASTERY: COMPLEX BODY GUARDS ---
@app.put("/update-profile/{user_id}")
async def update_user(
    # URL Guard: user_id must be positive
    user_id: Annotated[int, Path(ge=1)],
    
    # Body Guard: Validates the entire JSON object against UserProfile class
    user_data: UserProfile,
    
    # Standalone Body Guard: A single value hidden in the JSON body
    importance: Annotated[int, Body(gt=0, le=10)],
    
    # Query Guard: An optional URL flag (e.g., ?confirm=true)
    confirm: bool = Query(False)
):
    """
    ENGINEERING LOG:
    In Java, I'd print error messages manually. Here, if the code hits 
    this line, I KNOW the data is 100% clean because FastAPI 
    pre-validated it and would have sent a 422 error otherwise.
    """
    
    validated_packet = {
        "user_id": user_id,
        "profile": user_data,
        "priority_level": importance,
        "is_confirmed": confirm,
        "status": "Ready for Database"
    }

    # DAY 5 TEASER: We will soon use database.append(validated_packet)
    return validated_packet