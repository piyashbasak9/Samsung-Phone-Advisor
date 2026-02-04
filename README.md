# Samsung Phone Advisor API

A FastAPI-based REST API for Samsung phone recommendations powered by FREE Groq LLM (or OpenAI).

## Key Features

- 🚀 **Multi-LLM Support**: Groq (FREE) or OpenAI (PAID)
- 💰 **Free Option**: Groq API requires NO credit card
- ⚡ **Fast**: Groq is extremely fast (no credits needed)
- 🤖 **AI-Powered**: LLM-generated responses only (no hardcoded answers)
- 📱 **Samsung Focus**: Extract phone models and provide recommendations

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

## 🆓 Using FREE Groq LLM (Recommended)

Groq is **completely free** - no credit card needed!

### Step 1: Get Groq API Key

1. Go to: https://console.groq.com/keys
2. Sign up (free, takes 30 seconds)
3. Create API key (it starts with `gsk_`)
4. Copy the key

### Step 2: Configure `.env`

Edit `.env` file and add your Groq key:

```env
# LLM Provider Selection
LLM_PROVIDER=groq

# Groq API Configuration (FREE)
GROQ_API_KEY=gsk_YOUR_KEY_HERE
GROQ_MODEL=mixtral-8x7b-32768
```

### Step 3: Test Connection

```bash
# Test Groq connection
curl http://localhost:8000/test/openai
```

You should see: `"status": "success"`

### Step 4: Use the `/ask` endpoint

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Tell me about Galaxy S24 Ultra camera"}'
```

Now you'll get AI-generated responses using **FREE Groq**! ✅

## 💳 Using Paid OpenAI (Optional)

If you prefer OpenAI instead:

### Step 1: Get OpenAI API Key

1. Go to: https://platform.openai.com/api-keys
2. Create API key
3. Add payment method (credit/debit card)
4. Copy your key

### Step 2: Configure `.env`

```env
# Switch to OpenAI
LLM_PROVIDER=openai

# OpenAI Configuration
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
OPENAI_MODEL=gpt-4o-mini
```

### Step 3: Test Connection

```bash
curl http://localhost:8000/test/openai
```

## 📚 API Endpoints

### `/ask` - Main Advisor Endpoint
Provides Samsung phone recommendations using LLM.

```bash
POST /ask
Content-Type: application/json

{
  "question": "Tell me about Galaxy S24 Ultra camera"
}
```

**Response:**
```json
{
  "phone_model": "Galaxy S24 Ultra",
  "specs": {...},
  "review": "AI-generated response from Groq",
  "status": "success"
}
```

### `/llm` - Direct LLM Endpoint
Send any prompt to LLM and get response.

```bash
POST /llm
Content-Type: application/json

{
  "prompt": "Explain why Galaxy S24 Ultra is good for photography",
  "model": "mixtral-8x7b-32768",
  "max_tokens": 256,
  "temperature": 0.7
}
```

### `/llm/demo` - Demo Endpoint
Test without using any API quota.

```bash
POST /llm/demo
Content-Type: application/json

{
  "prompt": "Any question here"
}
```

**Response:**
```json
{
  "response": "[DEMO MODE] Sample response...",
  "demo": true
}
```

### `/test/openai` - Diagnostics
Check if your configured LLM provider is working.

```bash
GET /test/openai
```

Returns detailed status and troubleshooting info.

## 🔧 Troubleshooting

### "GROQ_API_KEY not set"
→ Add `GROQ_API_KEY=gsk_...` to `.env` and restart server

### "OpenAI Quota Exceeded"
→ Switch to FREE Groq (set `LLM_PROVIDER=groq`)

### API not responding
→ Run: `curl http://localhost:8000/test/openai`

## 📖 Development

### Install development tools
```bash
pip install pytest pytest-asyncio black flake8
```

### Format code
```bash
black .
```

### Lint code
```bash
flake8 .
```

## 💡 Why Groq is Recommended

| Feature | Groq | OpenAI |
|---------|------|--------|
| **Cost** | FREE ✅ | PAID |
| **Credit Card** | NOT needed ✅ | Required |
| **Speed** | ⚡ Very Fast | Good |
| **Model** | Mixtral 8x7B | GPT-4o-mini |
| **Setup** | 30 seconds | Requires billing |

## License

MIT License


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
