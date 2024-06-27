from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from pathlib import Path
import uvicorn

app = FastAPI()

IMAGE_DIR = Path("images")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

##############################################################

@app.get("/")
def home():
    return {'localhst:8000/docs'}


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_location = IMAGE_DIR / file.filename
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"info": f"File '{file.filename}' uploaded successfully"}

@app.get("/download/{filename}")
async def download_image(filename: str):
    file_location = IMAGE_DIR / filename
    if file_location.is_file():
        return FileResponse(file_location)
    return {"error": "File not found"}

@app.get("/files")
async def list_files():
    files = [f.name for f in IMAGE_DIR.iterdir() if f.is_file()]
    return {"files": files}

##############################################################

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)