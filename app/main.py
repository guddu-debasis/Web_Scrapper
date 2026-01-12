import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv

# Absolute Import: This tells Python to look inside the 'app' package
from app.routes import api_routes

# 1. Load environment variables
load_dotenv()

app = FastAPI(title="AI RAG Summarizer")

# 2. Configure CORS (Cross-Origin Resource Sharing)
# Essential for allowing your browser UI to call your Python API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "https://web-scrapper-o1vg.onrender.com",
        "*"
        ],  # For production, replace "*" with your specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Handle Absolute Paths for the 'static' folder
# This prevents the "Directory 'static' does not exist" error
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Ensure the static directory exists before mounting
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)
    print(f"Created missing directory: {STATIC_DIR}")

from app.config.db import client

@app.on_event("startup")
async def startup_db_client():
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"FATAL: Could not connect to MongoDB. Error: {e}")


# 4. Include API Routes (Auth, Summarize)
app.include_router(api_routes.router)

# 5. Mount Static Files
# Files in /static are now accessible at http://localhost:8000/static/
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# 6. Serve the UI at the Root URL (/)
@app.get("/")
async def read_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

# 7. Start the Server
if __name__ == "__main__":
    import uvicorn
    # Using 0.0.0.0 makes the server accessible on your local network
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)