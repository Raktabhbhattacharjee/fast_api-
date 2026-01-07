from fastapi import FastAPI
from pydantic import BaseModel, Field

# 1. THE SCHEMA (The Gatekeeper)
class FileUpload(BaseModel):
    filename: str
    content_type: str
    size_mb: float = Field(gt=0, description="Size must be positive")
    is_public: bool = False

app = FastAPI()

# MOCK DATABASE (Simulating your storage)
storage_metadata = {}

@app.post("/upload/{user_id}")
async def process_user_upload(
    user_id: int,                   # PATH: Who is uploading?
    upload: FileUpload,             # BODY: The JSON data
    category: str = "general",      # QUERY: Optional category
    secret_key: str | None = None   # QUERY: For authentication
):
    """
    ## 🎯 The Main Logic Function
    This route handles the entire data lifecycle:
    1. Validates the JSON Body (Pydantic)
    2. Checks the Secret Key (Logic)
    3. Merges all data into a Dictionary (model_dump)
    4. "Saves" it to our mock DB
    """
    
    # 1. SECURITY LOGIC
    if secret_key != "2026_CORE":
        return {"error": "Unauthorized Access", "status": 401}

    # 2. DATA TRANSLATION (The Bridge)
    # We dump to dict so we can use Python's logic power
    file_dict = upload.model_dump()
    
    # 3. ARCHITECTURE: Merging Path and Query into our data
    file_dict.update({
        "owner_id": user_id,
        "folder": category,
        "server_status": "synced"
    })
    
    # 4. MOCK STORAGE: Saving by user_id
    storage_metadata[user_id] = file_dict

    return {
        "message": "File metadata processed successfully",
        "data": file_dict,
        "so_yea": "Boilerplate done, Logic complete!"
    }