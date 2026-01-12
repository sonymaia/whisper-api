from fastapi import FastAPI, UploadFile, File, Header, HTTPException
import whisper
import os
import uuid

app = FastAPI()

model = whisper.load_model("base")

@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    x_api_key: str = Header(None)
):
    if x_api_key != os.getenv("WHISPER_API_KEY"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    filename = f"/tmp/{uuid.uuid4()}_{file.filename}"

    with open(filename, "wb") as f:
        f.write(await file.read())

    result = model.transcribe(filename, language="pt")

    os.remove(filename)

    return {
        "text": result["text"]
    }
