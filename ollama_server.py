from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

# Initialize FastAPI
app = FastAPI()

# Allow requests from GitHub Pages + Vite dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://alshehrimazen.github.io", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Replace with your actual OpenRouter API key
OLLAMA_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": "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",  # << REPLACE THIS
    "Content-Type": "application/json"
}

# Request body
class PlanRequest(BaseModel):
    user_input: str

@app.post("/generate_plan")
def generate_plan(req: PlanRequest):
    prompt = f"""
Create Umrah plan in **Makkah only**.

Each day must include:
- Morning, Afternoon, Evening, and Night activities
- Visits to Islamic sites like Masjid al-Haram, Jabal al-Nour
- Local restaurant and hotel suggestions

Do not mention other cities. Format the output using Markdown headers and bullet points.

Budget summary at the end.

User input:
{req.user_input}
"""

    payload = {
        "model": "mistralai/mixtral-8x7b",  # You can change the model
        "messages": [
            {"role": "system", "content": "You are an Umrah travel planner."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(OLLAMA_URL, headers=HEADERS, json=payload)

        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            return {"response": content}
        else:
            return {"error": f"Ollama error: {response.status_code} - {response.text}"}

    except Exception as e:
        return {"error": f"Exception while connecting to Ollama: {str(e)}"}
