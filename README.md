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
