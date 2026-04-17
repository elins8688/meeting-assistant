import requests
import config
import json

def build_prompt(transcript):
    return f"""
You are an AI meeting assistant. Analyze the transcript and extract
1. A consice summary (maximum of 5 sentences)
2. Key topics and keywords
3. Action topics with owner if mentioned

Transcript:
{transcript}
Respond ONLY with valid JSON in this format:

{{
    "summary":"...",
    "keywords": ["keyword1","keyword2"],
    "action_items": ["action1","action2"]
}}
"""
def call_ollama(prompt):
    try:
        response = requests.post(
            config.OLLAMA_URL,
            json={
                "model":config.MODEL,
                "prompt":prompt,
                "stream": False,
                "format": "json"
            }
        )
        data = response.json()
        
        if "response" not in data:
            raise ValueError(f"Unexpected response: {data}")
        
        return json.loads(data["response"])
    
    except Exception as e:
        return {
            "error":str(e)
        }