# Isotopes

A lightweight local AI workflow that connects a Telegram bot to a FastAPI bridge, which then forwards prompts to Ollama.

## Overview

This project has two main services:

- `bridge/app.py` runs a FastAPI app and exposes a `/chat` endpoint.
- `bot/bot.py` listens for Telegram messages and forwards them to the bridge.
- The bridge calls Ollama using the configured model and returns the generated response.

## Prerequisites

Before starting, make sure you have:

- Python 3.10+
- `pip` installed
- Ollama installed and running locally
- A Telegram bot token from BotFather
- A model already available in Ollama (for example `qwen3.5:2b`)

## Quick start

### 1) Create a virtual environment

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure environment variables

Copy the example file and edit it:

```bash
cp .env.example .env
```

Then set your values in `.env`:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen3.5:2b
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
BOT_PORT=8080
```

Notes:
- `OLLAMA_BASE_URL` should point to your local Ollama server.
- `OLLAMA_MODEL` must match a model already downloaded in Ollama.
- `TELEGRAM_BOT_TOKEN` is required for the bot to run.

### 4) Start Ollama

If Ollama is not running yet:

```bash
ollama serve
```

Then make sure the model is installed:

```bash
ollama pull qwen3.5:2b
```

If you use a different model, update `OLLAMA_MODEL` in `.env` accordingly.

### 5) Start the bridge service

The bot currently sends requests to `http://localhost:8001/chat`, so the bridge must be running on port `8001` before the bot starts.

```bash
uvicorn bridge.app:app --host 0.0.0.0 --port 8001
```

This starts the FastAPI app that receives `/chat` requests and forwards them to Ollama.

### 6) Start the Telegram bot

Open a second terminal and run:

```bash
python bot/bot.py
```

Once the bot is running, send `/start` to your Telegram bot to confirm it is live.

## End-to-end workflow

1. A user sends a message to the Telegram bot.
2. The bot posts that message to `http://localhost:8001/chat`.
3. The FastAPI bridge sends the message to Ollama using the configured model.
4. Ollama returns the answer.
5. The answer is sent back to the Telegram bot and displayed to the user.

## Recommended startup order

Use this exact sequence:

```bash
# Terminal 1
ollama serve

# Terminal 2
uvicorn bridge.app:app --host 0.0.0.0 --port 8001

# Terminal 3
python bot/bot.py
```

## Troubleshooting

### Bot says it cannot reach the local model bridge

Make sure the bridge is still running on port `8001`:

```bash
uvicorn bridge.app:app --host 0.0.0.0 --port 8001
```

### No response from Ollama

Check that Ollama is running and the model is installed:

```bash
ollama serve
ollama list
```

### Bot does not start

Verify your `.env` file contains a valid `TELEGRAM_BOT_TOKEN`.

## Project files

- `bridge/app.py` — FastAPI bridge used to call Ollama
- `bot/bot.py` — Telegram bot logic
- `.env.example` — sample environment configuration
- `requirements.txt` — Python package dependencies
