from fastapi import FastAPI
from pydantic import BaseModel
from llm import build_prompt,call_ollama
from fastapi import HTTPException

app = FastAPI()

class TranscriptRequest(BaseModel):
    transcript: str
    
@app.get("/")
def root():
    return {"message": "Meeting assistant API is running."}

@app.post("/analyze_transcript")
def analyze_transcript(request: TranscriptRequest):
    try:
        if not request.transcript.strip():
            raise HTTPException(status_code=422,detail="Transcript is empty")
        
        prompt = build_prompt(request.transcript)
        
        result = call_ollama(prompt)
        
        required_keys = {"summary","keywords","action_items"}
        missing_keys = required_keys - result.keys()
        if missing_keys:
            raise ValueError(f"Missing key in LLM response: {missing_keys}")
        
        return {
            "result":result
        }
    except Exception as e:
        raise HTTPException(staus_code=500,detail= str(e))