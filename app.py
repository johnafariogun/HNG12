from fastapi import FastAPI
from datetime import datetime
from pytz import timezone
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET"],
        allow_headers=["*"],
        allow_credentials=True,
    )
@app.get('/')
async def get_info():
    current_datetime = datetime.now(timezone('UTC')).isoformat()

    return {
        "email": "afariogunjohn2502@gmail.com",
        "current_datetime": current_datetime,
        "github_url": "https://github.com/johnafariogun/HNG12.git"
    }