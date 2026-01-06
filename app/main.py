from enum import Enum

from fastapi import FastAPI

class Myteam(Enum):
    me = "gemini"
    user = "developer"

app=FastAPI()

@app.get("/whois/{name}")

async def get_team(name:Myteam):
    
    #  if they are presnet show them 
    if name==Myteam.me:
        return{"full_name":"gemini_ai","role":"developer"}
    