import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

# Load env from project root: ~/isotope/.env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Load LLM details
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
BOT_PORT = os.getenv("BOT_PORT", "8080")

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    chat_id: str
    user_id: str


@app.post("/chat")
async def chat(req: ChatRequest):
    generate_url = f"{OLLAMA_BASE_URL.rstrip('/')}/api/generate"

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": req.message,
        "stream": False,
    }

    try:
        response = httpx.post(generate_url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        reply = data.get("response", "").strip()
    except Exception as exc:
        reply = f"Error contacting Ollama: {exc}"

    return {
        "text": reply or "I did not get a response from Ollama."
    }
