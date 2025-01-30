from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://hng12-owcr.onrender.com"],
        allow_methods=["GET"],
        allow_headers=["*"],
        allow_credentials=True,
    )

@app.exception_handler(HTTPException)
async def redirect_home(request, exc):
    if exc.stattus_code == 404:
        return RedirectResponse(url='/')
    return await app.default_exception_handler(request, exc)

@app.get('/')
async def get_info():
    current_datetime = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    return {
        "email": "afariogunjohn2502@gmail.com",
        "current_datetime": current_datetime,
        "github_url": "https://github.com/johnafariogun/HNG12"
    }

