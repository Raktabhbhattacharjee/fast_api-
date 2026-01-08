from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(
    # --- LEVEL 1, 2 & 4 (Strings & Lists) ---
    # THINK: Annotated is a wrapper for Metadata. Python ignores it; FastAPI reads it.
    # TYPE: list[str] | None means it acts like a std::vector<string> that can be null.
    q: Annotated[
        list[str] | None, 
        Query(
            # LEVEL 1: PLUMBING
            alias="item-query",      # The "Public" name in the URL (?item-query=...)
            title="Search Term",     # Label used in Swagger UI
            min_length=3,            # VALIDATION: Each string must be >= 3 chars
            max_length=50,           # VALIDATION: Each string must be <= 50 chars
            
            # LEVEL 2: REGEX (The "Stencil")
            # ONLY allow letters and spaces. No numbers or dots.
            pattern="^[a-zA-Z\s]+$" 
        )
    ] = None, # = None makes it optional. 

    # --- LEVEL 3 (Numeric Constraints) ---
    # THINK: These are "Range Guards."
    size: Annotated[
        int, 
        Query(
            ge=1,   # Greater than or Equal to 1 (No zeros/negatives)
            le=100  # Less than or Equal to 100 (Prevent server-side strain)
        )
    ] = 10 # Default value is 10
):
    # AT THIS POINT: The data is already "Sanitized." 
    # If q exists, it's guaranteed to be a list of clean strings.
    # If size exists, it's guaranteed to be between 1 and 100.
    
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    
    results.update({"page_size": size})
    
    if q:
        # In the URL, this was ?item-query=A&item-query=B
        # In Python, q is now ['A', 'B']
        results.update({"active_filters": q})
        
    return results