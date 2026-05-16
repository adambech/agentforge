from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from typing import Optional
from prompt_builder import build_prompt
from bob_runner import run_bob, collect_files
from file_parser import extract_files_simple
from zipper import create_zip
import subprocess
import os
import uuid

app = FastAPI(title="AgentForge", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    description: str
    auth: Optional[bool] = True
    audit: Optional[bool] = True
    frontend: Optional[str] = "webchat"
    llm: Optional[str] = "gemini"

class DownloadFilesRequest(BaseModel):
    files: dict[str, str]

@app.get("/")
def root():
    return {"message": "AgentForge API is running"}

@app.post("/generate")
def generate(req: GenerateRequest):
    import tempfile
    import os
    import uuid
    
    prompt = build_prompt(
        description=req.description,
        auth=req.auth,
        audit=req.audit,
        frontend=req.frontend,
        llm=req.llm
    )
    
    # Use permanent directory instead of temp
    work_dir = f"/tmp/agentforge_{uuid.uuid4().hex[:8]}"
    os.makedirs(work_dir, exist_ok=True)
    
    subprocess.run(["git", "init"], cwd=work_dir, capture_output=True)
    subprocess.run(["git", "commit", "--allow-empty", "-m", "init"], cwd=work_dir, capture_output=True)
    
    try:
        bob_output = run_bob(prompt, work_dir)
    except Exception as e:
        bob_output = str(e)
    
    files = collect_files(work_dir)
    
    if not files:
        files = extract_files_simple(bob_output)
    
    if not files:
        return {"error": "Bob did not generate any files", "raw_output": bob_output, "work_dir": work_dir}
    
    return {
        "files": files,
        "file_count": len(files),
        "filenames": list(files.keys()),
        "work_dir": work_dir
    }

@app.post("/generate/download")
def generate_and_download(req: GenerateRequest):
    prompt = build_prompt(
        description=req.description,
        auth=req.auth,
        audit=req.audit,
        frontend=req.frontend,
        llm=req.llm
    )
    
    work_dir = f"/tmp/agentforge_{uuid.uuid4().hex[:8]}"
    os.makedirs(work_dir, exist_ok=True)
    subprocess.run(["git", "init"], cwd=work_dir, capture_output=True)
    subprocess.run(["git", "commit", "--allow-empty", "-m", "init"], cwd=work_dir, capture_output=True)
    
    try:
        bob_output = run_bob(prompt, work_dir)
    except Exception as e:
        bob_output = str(e)
    
    files = collect_files(work_dir)

    if not files:
        return {"error": "Bob did not generate any files"}

    zip_bytes = create_zip(files)
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=agentforge-project.zip"}
    )

@app.post("/generate/download-files")
def download_files(req: DownloadFilesRequest):
    zip_bytes = create_zip(req.files)
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=agentforge-project.zip"}
    )