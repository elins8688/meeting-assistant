from fastapi import FastAPI
from pydantic import BaseModel
from llm import build_prompt,call_ollama

app = FastAPI()

class TranscriptRequest(BaseModel):
    transcript: str
    
@app.get("/")
def root():
    return {"message": "Meeting assistant API is running."}

@app.post("/analyze_transcript")
def analyze_transcript(request: TranscriptRequest):
    prompt = build_prompt(request.transcript)
    result = call_ollama(prompt)
    return {
        "result":result
    }