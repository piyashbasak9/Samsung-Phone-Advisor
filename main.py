import os
import re
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from db_setup import fetch_all_phones, fetch_phone_by_model

# 1. Setup Environment & AI
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if not GOOGLE_API_KEY:
    raise ValueError("Error: GOOGLE_API_KEY is missing in .env file")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Initialize App
app = FastAPI(
    title="Samsung Advisor API",
    description="Backend for Samsung Phone Recommendation System",
    version="1.0.0"
)

# 3. Pydantic Models
class UserQuery(BaseModel):
    question: str

class AdviceResponse(BaseModel):
    phone_model: str
    specs: dict
    review: str

# 4. Helper: Extract Model Name using Regex (Agent 1 Logic)
def extract_model_name(question: str) -> str:
    # Patterns to catch common names like "S24 Ultra", "A55", "Z Fold 5"
    patterns = [
        r'Galaxy\s+S\d+(?:\s+Ultra|\s+Plus)?', 
        r'Galaxy\s+Z\s+(?:Fold|Flip)\s+\d+', 
        r'Galaxy\s+A\d+', 
        r'S\d+\s+Ultra',
        r'S\d+\s+Plus',
        r'S\d+'
    ]
    for pattern in patterns:
        match = re.search(pattern, question, re.IGNORECASE)
        if match:
            return match.group(0).strip()
    return ""

# 5. Helper: Generate AI Review (Agent 2 Logic)
def generate_ai_review(specs: dict, user_question: str) -> str:
    context = f"""
    Phone: {specs['model_name']}
    Price: {specs['price']}
    Display: {specs['display']}
    Camera: {specs['camera']}
    Battery: {specs['battery']}
    """
    
    prompt = f"""
    You are a helpful phone assistant. 
    User Question: "{user_question}"
    
    Tech Specs:
    {context}
    
    Task: Write a short, natural, and helpful answer (max 3 sentences) based on the specs.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "I found the specs, but I couldn't generate a review due to a network issue."

# ============================================================================
# API ROUTES
# ============================================================================

@app.get("/")
def home():
    return {"status": "Active", "message": "Samsung Advisor API is running"}

# Route 1: Get list of all phones
@app.get("/phones", tags=["Database"])
def get_all_phones():
    phones = fetch_all_phones()
    return {"count": len(phones), "phones": phones}

# Route 2: Get details of a specific phone
@app.get("/phones/{model_name}", tags=["Database"])
def get_phone_details(model_name: str):
    specs = fetch_phone_by_model(model_name)
    if not specs:
        raise HTTPException(status_code=404, detail="Phone not found")
    return {"phone": specs}

# Route 3: Ask the AI Assistant
@app.post("/ask", response_model=AdviceResponse, tags=["AI Agent"])
async def ask_question(query: UserQuery):
    # Step 1: Identify Model
    model_name = extract_model_name(query.question)
    
    if not model_name:
        raise HTTPException(status_code=400, detail="Please mention a specific Samsung model (e.g., S24 Ultra).")
    
    # Step 2: Retrieve Data
    specs = fetch_phone_by_model(model_name)
    
    if not specs:
        raise HTTPException(status_code=404, detail=f"Details for '{model_name}' not found in database.")
    
    # Step 3: Generate Review
    review = generate_ai_review(specs, query.question)
    
    return AdviceResponse(
        phone_model=specs['model_name'],
        specs=specs,
        review=review
    )