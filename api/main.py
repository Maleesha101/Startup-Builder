import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from controller.orchestrator import Orchestrator
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Startup Builder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator(output_dir="output")


class BuildRequest(BaseModel):
    idea: str


@app.post("/build")
async def build_startup(request: BuildRequest):
    if not os.getenv("GOOGLE_API_KEY"):
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY not set")

    # Run synchronously for prototype simplicity, or use background tasks for real async
    # For a deterministic demo, await it.
    try:
        results = await orchestrator.run_workflow(request.idea)
        return {"status": "success", "artifacts": results}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/artifacts/{filename}")
async def get_artifact(filename: str):
    file_path = os.path.join("output", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="Artifact not found")


@app.get("/")
async def read_root():
    return FileResponse("frontend/index.html")


app.mount("/static", StaticFiles(directory="frontend"), name="static")
