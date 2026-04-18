from fastapi.testclient import TestClient
from unittest.mock import patch
import httpx

from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.json()=={"message":"Meeting assistant API is running."}
    assert response.status_code == 200
    
def test_analyze_meeting_sucess():
    """A correct response returns summary, keywords and action_items"""
    
    mock_analysis = {
        "summary":"The team discussed deadlines and design reviews.",
        "keywords":["deadline","design review","report"],
        "action_items":["Alice to send report by Friday", "Jonathan to lead design review"]
        }
    mock_meeting_transcript = {
        "transcript":"""Jonathan: Alright, let’s get started. We need to align on deadlines and the upcoming design review.
        Priya: The current build is on track, but we’re tight on documentation. That could affect the final report.
        Mark: I agree. We should prioritize the report completion before final QA.
        Alice: I can take responsibility for compiling the report. I should be able to send a draft by Friday.
        Jonathan: Good. For the design review, I’ll lead it. We should schedule it early next week so we have buffer time.
        Priya: Sounds good. Also, we should make sure all feedback from stakeholders is included before that review.
        Mark: I’ll gather the latest stakeholder comments and send them to Jonathan.
        Jonathan: Perfect. So main focus is deadlines and ensuring the design review is well-prepared.
        Alice: Got it."""
    }
    with patch("app.main.analyze_transcript") as mock_llm:
        mock_llm.return_value = mock_analysis
        response = client.post("/analyze_transcript",json = mock_meeting_transcript)  
    assert response.status_code == 200
    data = response.json()["result"]
    
    assert "summary" in data
    assert "keywords" in data
    assert "action_items" in data
    assert isinstance(data["keywords"],list) 
    assert isinstance(data["action_items"],list) 
    
def test_empty_transcript():
    """Empty transcripts returns 422"""
    mock_meeting_transcript = {
        "transcript": " "
    }
    with patch("app.main.analyze_transcript") as mock_llm:
        response = client.post("/analyze_transcript",json = mock_meeting_transcript)
    assert response.status_code == 422
    mock_llm.assert_not_called()
    
def test_ollama_down():
    """When Ollama is not running return 500"""
    with patch("app.main.call_ollama") as mock_llm:
        mock_llm.side_effect= RuntimeError("Ollama is not running")
        
        response = client.post("/analyze_transcript",json = {"transcript": "Meeting content"})
        
    assert response.status_code == 500
    
    
    
    
    
    