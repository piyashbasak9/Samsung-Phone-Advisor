from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re
import os
from dotenv import load_dotenv
from db_setup import fetch_phone_by_model, get_db_connection
import psycopg2

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Samsung Smart Phone Advisor",
    description="Multi-Agent system for Samsung phone recommendations",
    version="1.0.0"
)

# Request/Response Models
class UserQuery(BaseModel):
    question: str


class PhoneSpecs(BaseModel):
    id: int
    model_name: str
    display: str
    battery: str
    camera: str
    ram: str
    storage: str
    price: str


class AdviceResponse(BaseModel):
    phone_model: str
    specs: dict
    review: str
    status: str





#AGENT 1: DATA EXTRACTOR

def extract_phone_model(question: str) -> str:
    
    print(f"[AGENT 1] Extracting phone model from: {question}")
    
    # Common Samsung phone patterns
    patterns = [
        r'Galaxy\s+S\d+(?:\s+Ultra)?',  
        r'Galaxy\s+Z\s+(?:Fold|Flip)\s+\d+',  
        r'Galaxy\s+A\d+',  
        r'Galaxy\s+Tab\s+S\d+',  
        r'S\d+\s+Ultra', 
        r'Z\s+(?:Fold|Flip)', 
    ]
    
    for pattern in patterns:
        match = re.search(pattern, question, re.IGNORECASE)
        if match:
            model = match.group(0).strip()
            print(f"[AGENT 1] ✓ Detected: {model}")
            return model
    
    print("[AGENT 1] ⚠ No phone model detected")
    return ""

def fetch_phone_specs(model_name: str) -> dict:
    print(f"[AGENT 1] Querying database for: {model_name}")
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # SQL query: ILIKE for case-insensitive search
        query = """
        SELECT id, model_name, display, battery, camera, ram, storage, price
        FROM smartphones
        WHERE model_name ILIKE %s
        LIMIT 1;
        """
        
        cursor.execute(query, (f'%{model_name}%',))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            specs = {
                'id': result[0],
                'model_name': result[1],
                'display': result[2],
                'battery': result[3],
                'camera': result[4],
                'ram': result[5],
                'storage': result[6],
                'price': result[7]
            }
            print(f"[AGENT 1] ✓ Found: {specs['model_name']}")
            return specs
        else:
            print(f"[AGENT 1] ✗ Phone not found in database")
            return None
            
    except psycopg2.OperationalError as e:
        print(f"[AGENT 1] ✗ Database error: {e}")
        return None





















# FASTAPI ENDPOINTS


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "Samsung Smart Phone Advisor",
        "version": "1.0.0"
    }


@app.post("/ask", response_model=AdviceResponse, tags=["Advisor"])
async def ask_advisor(query: UserQuery):
    
    print(f"\n{'='*70}")
    print(f"User Question: {query.question}")
    print(f"{'='*70}\n")
    
    # AGENT 1: Extract phone model
    phone_model = extract_phone_model(query.question)
    
    if not phone_model:
        raise HTTPException(
            status_code=400,
            detail="Could not detect a Samsung phone model in your question. "
                   "Please mention a specific model (e.g., S24 Ultra, Galaxy Z Fold 6)"
        )
    
    # AGENT 1: Fetch specs from database
    specs = fetch_phone_specs(phone_model)
    
    if not specs:
        raise HTTPException(
            status_code=404,
            detail=f"Sorry, I couldn't find detailed information about the {phone_model} in my database. "
                   "Please try another model or check the model name."
        )
    
    # Prepare response
    response = AdviceResponse(
        phone_model=specs['model_name'],
        specs={
            'display': specs['display'],
            'battery': specs['battery'],
            'camera': specs['camera'],
            'ram': specs['ram'],
            'storage': specs['storage'],
            'price': specs['price']
        },
        status="success"
    )
    
    print(f"\n✓ Response prepared successfully\n")
    return response



@app.get("/phones")
async def list_all_phones():
    """Get all available phones in the database"""
    


@app.get("/phones/{model_name}")
async def get_phone_details(model_name: str):
    """Get detailed specs for a specific phone"""
  


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("Samsung Smart Phone Advisor - FastAPI Server")
    print("\n🚀 Starting server on http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("\n" + "="*70 + "\n")
    
    # Run Uvicorn server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
