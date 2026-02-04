# Samsung Phone Advisor

An intelligent AI-powered backend system that provides personalized Samsung phone recommendations using Google's Gemini AI and FastAPI.

## Features

- **AI-Powered Recommendations**: Uses Google Gemini 2.5 Flash to analyze user queries and provide intelligent phone recommendations
- **Phone Database**: PostgreSQL database storing Samsung phone specifications (display, camera, battery, storage, price, color)
- **Regex-Based Model Extraction**: Intelligent extraction of phone model names from user queries
- **RESTful API**: FastAPI-based backend with clear endpoints for phone queries and recommendations
- **Web Scraping**: Data collection capabilities with BeautifulSoup for phone information gathering
- **Environment Management**: Secure configuration using .env files

## Tech Stack

- **Backend Framework**: FastAPI, Uvicorn
- **Database**: PostgreSQL with psycopg2
- **AI**: Google Generative AI (Gemini 2.5 Flash)
- **Web Scraping**: BeautifulSoup, Requests
- **Validation**: Pydantic
- **Configuration**: python-dotenv

## Project Structure

```
├── main.py              # FastAPI application & endpoints
├── db_setup.py          # Database configuration & queries
├── scraper.py           # Web scraping utilities
├── setup.py             # Package setup configuration
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Google Generative AI API key

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Samsung-Phone-Advisor
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   DB_NAME=samsung_phones
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   ```

5. **Setup database**
   ```bash
   python db_setup.py
   ```

## Usage

### Start the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Example Endpoints

#### Get All Phones
```bash
GET /phones
```

#### Get Phone by Model
```bash
GET /phones/{model_name}
```

#### Get AI Recommendation
```bash
POST /recommend
Content-Type: application/json

{
  "question": "What Samsung phone should I buy for photography?"
}
```

## API Response Example

```json
{
  "phone_model": "Galaxy S24 Ultra",
  "specs": {
    "display": "6.8\" AMOLED 120Hz",
    "camera": "200MP main camera",
    "battery": "5000mAh",
    "storage": "512GB",
    "price": "$1299"
  },
  "review": "The Galaxy S24 Ultra is perfect for photography enthusiasts with its advanced computational photography and AI features..."
}
```

## How It Works

1. **User Query**: User sends a question about Samsung phones
2. **Model Extraction**: Regex patterns extract phone model names from the query
3. **Database Lookup**: Fetch phone specifications from PostgreSQL
4. **AI Analysis**: Google Gemini analyzes the query and specifications
5. **Response**: Return personalized recommendation with specs and review

## Database Schema

The `phones` table contains:
- `id` (INTEGER, PRIMARY KEY)
- `model_name` (TEXT, UNIQUE)
- `display` (TEXT)
- `camera` (TEXT)
- `battery` (TEXT)
- `storage` (TEXT)
- `price` (TEXT)
- `color` (TEXT)

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GOOGLE_API_KEY` | Your Google Generative AI API key |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | PostgreSQL username |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | PostgreSQL host (default: localhost) |

## Development

### Running Tests
```bash
pytest tests/
```

### Code Structure

- **main.py**: Handles FastAPI endpoints and request processing
- **db_setup.py**: Database connection and query functions
- **scraper.py**: Web scraping utilities for data collection

## Future Enhancements

- [ ] Add comparison feature for multiple phones
- [ ] Implement user preference learning
- [ ] Add price tracking functionality
- [ ] Expand AI model capabilities
- [ ] Add caching for improved performance

## Troubleshooting

### Database Connection Error
Ensure PostgreSQL is running and credentials in `.env` are correct

### API Key Error
Verify `GOOGLE_API_KEY` is set in `.env` file

### Port Already in Use
Change port in startup command: `uvicorn main:app --port 8001`

## License

This project is licensed under the MIT License - see LICENSE file for details

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For issues or questions, please open an issue on the repository.

---

**Last Updated**: February 5, 2026
