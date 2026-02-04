from typing import Annotated, List, Optional
from fastapi import FastAPI, HTTPException, Path, Depends, status
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlalchemy.orm import sessionmaker

# --- 1. THE DATABASE ENGINE ---
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# connect_args={"check_same_thread": False} is REQUIRED for SQLite + FastAPI
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

# --- 2. THE SCHEMA ---
class UserProfile(SQLModel, table=True):
    # We set default=None so the user doesn't HAVE to send an ID in the POST request
    id: Optional[int] = Field(default=None, primary_key=True) 
    username: str = Field(index=True, min_length=3)
    age: int = Field(ge=18)

# --- 3. DATABASE SETUP & SESSION ---
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI(title="Day 7: Async-Ready SQL Persistence")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- 4. THE FIXED CRUD LOGIC (Async) ---

@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=UserProfile)
async def create_user(user: UserProfile, session: Session = Depends(get_session)):
    # Logic: We take the incoming 'user', add it to the session, and commit.
    session.add(user)
    session.commit()
    session.refresh(user) 
    return user

@app.get("/users/", response_model=List[UserProfile])
async def get_all_users(session: Session = Depends(get_session)):
    # select(UserProfile) creates the SQL query, session.exec runs it
    statement = select(UserProfile)
    results = session.exec(statement)
    return results.all()

@app.get("/users/{user_id}", response_model=UserProfile)
async def get_user(
    user_id: Annotated[int, Path(ge=0)], 
    session: Session = Depends(get_session)
):
    user = session.get(UserProfile, user_id)
    
    # This is where we "intercept" the empty result
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Sorry, User with ID {user_id} does not exist in our system."
        )
        
    return user

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: Annotated[int, Path(ge=0)], 
    session: Session = Depends(get_session)
):
    user = session.get(UserProfile, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(user)
    session.commit()
    return {"status": "Deleted successfully", "id": user_id}