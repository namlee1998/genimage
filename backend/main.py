import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from backend import aimusic

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Serve React build
# =========================
frontend_dir = os.path.join(os.path.dirname(__file__), "build")

# Serve frontend static (css, js)
app.mount("/static", StaticFiles(directory=os.path.join(frontend_dir, "static")), name="static")

# Serve generated files
app.mount("/generated", StaticFiles(directory="backend/generated"), name="generated")

# Serve React index.html (catch-all)
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    index_file = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "Frontend build not found"}

# =========================
# API routes (giữ nguyên logic)
# =========================
@app.post("/api/generate")
async def generate_music(prompt: str):
    return await aimusic.generate(prompt)
