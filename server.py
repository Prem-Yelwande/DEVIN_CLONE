from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import shutil
import tempfile
import os
from fastapi.middleware.cors import CORSMiddleware

from agents.graph import agent
from agents.tools import init_project_root, PROJECT_ROOT

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://devin-clone-oe17.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_project_root()


class PromptRequest(BaseModel):
    prompt: str


@app.post("/generate")
def generate(req: PromptRequest):
    try:
        agent.invoke(
            {"user_prompt": req.prompt, "mode": "new"},
            {"recursion_limit": 100}
        )
        return {"status": "done"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/edit")
def edit(req: PromptRequest):
    try:
        agent.invoke(
            {"user_prompt": req.prompt, "mode": "edit"},
            {"recursion_limit": 100}
        )
        return {"status": "done"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/reset")
def reset():
    shutil.rmtree(PROJECT_ROOT, ignore_errors=True)
    init_project_root()
    return {"status": "reset"}


@app.get("/download")
def download():
    if not PROJECT_ROOT.exists() or not any(PROJECT_ROOT.iterdir()):
        return {"status": "no_project"}

    tmp_dir = tempfile.mkdtemp()
    zip_base = os.path.join(tmp_dir, "project")
    zip_path = shutil.make_archive(zip_base, "zip", root_dir=PROJECT_ROOT)

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename="generated_project.zip"
    )


app.mount("/project", StaticFiles(directory=str(PROJECT_ROOT), html=True), name="project")
app.mount("/", StaticFiles(directory="static", html=True), name="static")