# Creates the FastAPI app and defines the endpoints

from fastapi import FastAPI
from pydantic import BaseModel
from app.llm import build_prompt,call_ollama
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
        # Empty transcript returns 422"
        if not request.transcript.strip():
            raise HTTPException(status_code=422,detail="Transcript is empty")
        
        prompt = build_prompt(request.transcript)
        
        result = call_ollama(prompt)
        
        # The LLM should always return these three keys based on the prompt
        # If any key is missing, treat as server error
        required_keys = {"summary","keywords","action_items"}
        missing_keys = required_keys - result.keys()
        if missing_keys:
            raise ValueError(f"Missing key in LLM response: {missing_keys}")
        
        return {
            "result":result
        }
    except HTTPException:
        # Re-raise HTTPException before the generic exception handler catches it
        raise

    except Exception as e:
        raise HTTPException(status_code=500,detail= str(e))