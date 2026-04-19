# Meeting-Assistant API
An LLM-powered meeting assistant that analyzes meeting transcripts and extracts:
- summary
- keywords
- action items

Built using a local LLM via Ollama, with a REST API powered by FastAPI.

## How it works 
Transcript -> LLM (Ollama) -> Summary, Keywords, Action items

## Project structure
```
meeting-api/
├── app/
│   ├── config.py   # Loads settings from .env
│   ├── llm.py      # Ollama integration and prompt logic
│   └── main.py     # FastAPI app and endpoint
├── tests/
│   └── test_main.py   # API tests
├── Dockerfile
├── requirements.txt
└── README.md
```

## Setup & Installation
1. Clone the repository and install rependencies
```bash
git clone https://github.com/elins8688/meeting-api.git
cd meeting-api
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
2. Configure environment
``` bash
cp .env.example .env
```

3. Install and start Ollama model
```bash 
ollama pull llama3
ollama serve
```

5. Start the API
```bash
uvicorn app.main:app --reload
```
The API is now running at http://localhost:8000
Auto-generated docs are at http://localhost:8000/docs

## Usage
Example request: 
```bash
curl -X POST http://localhost:8000/analyze-meeting \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Alice will send the report by Friday. Bob owns the design review."}'
```

Example response:
``` json
{
  "summary": "The team discussed project deadlines and assigned task owners.",
  "keywords": ["report", "design review", "deadline"],
  "action_items": [
    "Alice to send report by Friday",
    "Bob to lead the design review"
  ]
}
```
## Run tests
```bash
pytest tests/
```
## Running with Docker
```bash
docker build -t meeting-assistant .
docker run -p 8000:8000 meeting-assistant
```
> **Note:** When running via Docker, Ollama must be reachable from inside 
> the container. Update your `.env` depending on your operating system:
>
> **Mac/Windows:**
> `OLLAMA_URL=http://host.docker.internal:11434/api/generate`
>
> **Linux:**
> `OLLAMA_URL=http://172.17.0.1:11434/api/generate`