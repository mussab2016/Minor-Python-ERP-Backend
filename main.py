from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from http_server.http import api_router  # your router
import uvicorn

app = FastAPI(title="ERP Backend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register router
app.include_router(api_router)

if __name__ == "__main__":
    init_db()
    uvicorn.run("main:app", host="127.0.0.1", port=8787, reload=True)
