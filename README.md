# Samsung Phone Advisor API

A FastAPI-based REST API for Samsung phone recommendations and advisement.

## Project Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Using the LLM endpoint

This project includes a direct LLM endpoint at `/llm` which forwards a prompt to an OpenAI model.

#### Setup

1. Set your OpenAI API key in the environment or a `.env` file:

```bash
export OPENAI_API_KEY="sk-..."
# optionally set a model name
export OPENAI_MODEL="gpt-4o-mini"
```

Or add to `.env`:
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```

2. Run the server:

```bash
python main.py
```

#### Using the `/llm` endpoint (production)

Send a POST request with a prompt:

```bash
POST /llm
Content-Type: application/json

{
  "prompt": "Explain why Galaxy S24 Ultra is good for photography",
  "model": "gpt-4o-mini",
  "max_tokens": 256,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "model": "gpt-4o-mini",
  "response": "...",
  "demo": false
}
```

#### Using the `/llm/demo` endpoint (for testing without quota usage)

If you hit OpenAI API quota limits, use the demo endpoint to test your integration:

```bash
POST /llm/demo
Content-Type: application/json

{
  "prompt": "Explain why Galaxy S24 Ultra is good for photography"
}
```

**Response:**
```json
{
  "model": "gpt-4o-mini",
  "response": "[DEMO MODE] This is a sample LLM response...",
  "demo": true,
  "note": "This is a demo response. Use /llm endpoint for real API calls."
}
```

#### Error Handling

- **402 Payment Required**: OpenAI API quota exceeded. Check your [OpenAI billing](https://platform.openai.com/account/billing/overview).
- **500 Internal Server Error**: Other API or configuration errors.
- **OPENAI_API_KEY not set**: Set the key in `.env` or environment variables.

### API Documentation

Once the server is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Project Structure

```
.
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## Development

### Install development tools (optional)
```bash
pip install pytest pytest-asyncio black flake8
```

### Run tests
```bash
pytest
```

### Format code
```bash
black .
```

### Lint code
```bash
flake8 .
```

## License

MIT License
