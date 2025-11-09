# Small CLI AI assistant
This repository contains a minimal command-line assistant implemented in `main.py`.

Features
- Local rule-based mode (default) — works without any API keys.
- Optional OpenAI integration — set `OPENAI_API_KEY` in your environment to enable.

Quick start

1. (Optional) create a virtual environment and install requirements:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. Run the assistant:

```powershell
python main.py
```

3. Commands inside the assistant:
- `/help` show help
- `/history` show last interactions
- `/mode` show current mode (local or openai)
- `/exit` exit the assistant

OpenAI mode

1. Set the environment variable `OPENAI_API_KEY` to your API key (PowerShell example):

```powershell
$env:OPENAI_API_KEY = 'sk-...'
python main.py
```

Notes
- This is intentionally small and self-contained. Extend it by adding more local rules or swapping the OpenAI client for another provider.