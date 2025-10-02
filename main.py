import threading
import webbrowser

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from http_server.http import api_router  # your router
import uvicorn
from fastapi.staticfiles import StaticFiles
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

# Mount Angular dist folder as frontend
app.mount("/", StaticFiles(directory="erp-frontend/browser", html=True), name="frontend")

def start_server():
    init_db()
    uvicorn.run(app, host="127.0.0.1", port=8787)

if __name__ == "__main__":
    # Open browser after short delay
    threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:8787")).start()
    start_server()

# if __name__ == "__main__":
#     # Mount Angular dist
#     init_db()
#     uvicorn.run("main:app", host="127.0.0.1", port=8787, reload=True)
