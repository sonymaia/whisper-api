from fastapi import FastAPI, UploadFile, File
import whisper
import os
import uuid

app = FastAPI()

model = whisper.load_model("small")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    filename = f"/tmp/{uuid.uuid4()}_{file.filename}"

    with open(filename, "wb") as f:
        f.write(await file.read())

    result = model.transcribe(filename, language="pt")

    os.remove(filename)

    return {
        "text": result["text"]
    }
