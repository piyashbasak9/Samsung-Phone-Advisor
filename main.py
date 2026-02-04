
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


# LLM direct request model
class LLMRequest(BaseModel):
    prompt: str
    model: str | None = None
    max_tokens: int | None = 256
    temperature: float | None = 0.7







# AGENT 1: DATA EXTRACTOR

def extract_phone_model(question: str) -> str:
    print(f"[AGENT 1] Extracting phone model from: {question}")
    
    # Common Samsung phone patterns
    patterns = [
        r'Galaxy\s+S\d+(?:\s+Ultra)?',  # S24, S24 Ultra, etc.
        r'Galaxy\s+Z\s+(?:Fold|Flip)\s+\d+',  # Fold 6, Flip 6, etc.
        r'Galaxy\s+A\d+',  # A55, A35, etc.
        r'Galaxy\s+Tab\s+S\d+',  # Tab S10, etc.
        r'S\d+\s+Ultra',  # S23 Ultra
        r'Z\s+(?:Fold|Flip)',  # Z Fold, Z Flip
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



# AGENT 2: REVIEW GENERATOR

def call_llm_api(phone_specs: dict, user_question: str) -> str:
    
    print("[AGENT 2] Generating review using LLM...")
    
    # Build context for LLM
    specs_text = f"""
    Model: {phone_specs['model_name']}
    Display: {phone_specs['display']}
    Battery: {phone_specs['battery']}
    Camera: {phone_specs['camera']}
    RAM: {phone_specs['ram']}
    Storage: {phone_specs['storage']}
    Price: {phone_specs['price']}
    """
    
    # LLM Prompt
    prompt = f"""
    You are a helpful Samsung phone advisor. Here are the specifications for a phone:
    
    {specs_text}
    
    User's Question: {user_question}
    
    Provide a concise, natural language response that answers the user's question based on these specs.
    Be friendly, informative, and highlight key features relevant to the user's inquiry.
    Keep the response to 2-3 sentences maximum.
    """
    
    # Check if OpenAI API key is available
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    if openai_api_key:
        # Use actual OpenAI API (requires 'openai' package)
        try:
            from openai import OpenAI
            client = OpenAI(api_key=openai_api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            review = response.choices[0].message.content.strip()
            print("[AGENT 2] ✓ Review generated via OpenAI API")
            return review
            
        except ImportError:
            print("[AGENT 2] ⚠ OpenAI package not installed, using placeholder")
        except Exception as e:
            print(f"[AGENT 2] ⚠ OpenAI API error: {e}, using placeholder")
    
    # Placeholder LLM response (fallback)
    review = generate_placeholder_review(phone_specs, user_question)
    print("[AGENT 2] ✓ Review generated (placeholder mode)")
    return review


def generate_placeholder_review(phone_specs: dict, user_question: str) -> str:
    model = phone_specs['model_name']
    display = phone_specs['display']
    camera = phone_specs['camera']
    battery = phone_specs['battery']
    price = phone_specs['price']
    
    # Simple contextual responses
    if 'camera' in user_question.lower() or 'photo' in user_question.lower():
        return (f"The {model} features an excellent {camera} camera setup, making it ideal for photography enthusiasts. "
                f"With its premium sensor and computational photography, it delivers stunning images in various lighting conditions.")
    
    elif 'battery' in user_question.lower() or 'charge' in user_question.lower():
        return (f"The {model} comes with {battery}, ensuring excellent daily battery life. "
                f"The fast charging capability means you can get back to using your phone quickly.")
    
    elif 'display' in user_question.lower() or 'screen' in user_question.lower():
        return (f"The {model} boasts a beautiful {display} display that provides vibrant colors and smooth scrolling. "
                f"This makes it perfect for watching content and gaming.")
    
    elif 'price' in user_question.lower() or 'cost' in user_question.lower() or 'value' in user_question.lower():
        return (f"At {price}, the {model} offers excellent value with premium specs including {display} and {camera}. "
                f"It's a solid investment for anyone looking for a high-end Samsung experience.")
    
    elif 'review' in user_question.lower() or 'opinion' in user_question.lower():
        return (f"The {model} is an excellent smartphone featuring {display}, {camera}, and {battery}. "
                f"At {price}, it represents Samsung's commitment to premium features and reliable performance.")
    
    else:
        # Default response
        return (f"The {model} is a fantastic choice with impressive specifications including {display}, "
                f"{camera}, and {battery}. Priced at {price}, it offers great value and performance.")



def call_openai_prompt(prompt: str, model: str | None = None, max_tokens: int = 256, temperature: float = 0.7, demo_mode: bool = False) -> str:
    """Call OpenAI chat completion with a raw prompt and return text. If demo_mode=True, returns mock response."""
    if demo_mode:
        return f"[DEMO MODE] This is a sample LLM response. In production, the model would analyze: '{prompt[:100]}...'"
    
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. Set it in your environment or .env file.")

    use_model = model or os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

    try:
        from openai import OpenAI

        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model=use_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        text = response.choices[0].message.content.strip()
        return text

    except Exception as e:
        error_msg = str(e)
        if "insufficient_quota" in error_msg.lower() or "quota" in error_msg.lower():
            raise RuntimeError(
                "OpenAI API quota exceeded. Please check your OpenAI account billing at https://platform.openai.com/account/billing/overview. "
                "You can also use demo_mode=true for testing."
            )
        elif "401" in error_msg or "unauthorized" in error_msg.lower():
            raise RuntimeError("OpenAI API key is invalid. Please verify your OPENAI_API_KEY in .env")
        else:
            raise RuntimeError(f"OpenAI API call failed: {e}")



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
    
    # AGENT 2: Generate review
    review = call_llm_api(specs, query.question)
    
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
        review=review,
        status="success"
    )
    
    print(f"\n✓ Response prepared successfully\n")
    return response


@app.get("/phones", tags=["Database"])
async def list_all_phones():
    """Get all available phones in the database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT model_name, price FROM smartphones ORDER BY model_name;")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        phones = [{"model": row[0], "price": row[1]} for row in results]
        return {"count": len(phones), "phones": phones}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/phones/{model_name}", tags=["Database"])
async def get_phone_details(model_name: str):
    """Get detailed specs for a specific phone"""
    specs = fetch_phone_specs(model_name)
    
    if not specs:
        raise HTTPException(
            status_code=404,
            detail=f"Phone model '{model_name}' not found in database"
        )
    
    return {"phone": specs}



@app.post("/llm", tags=["LLM"])
async def llm_query(req: LLMRequest):
    """Direct LLM endpoint. Returns the model's text reply to a raw prompt.
    
    Use demo=true query parameter to test without hitting OpenAI API quota.
    """
    try:
        # Check if demo mode is requested (for testing without quota issues)
        import inspect
        frame = inspect.currentframe()
        demo_mode = False
        
        text = call_openai_prompt(
            req.prompt, 
            model=req.model, 
            max_tokens=req.max_tokens or 256, 
            temperature=req.temperature or 0.7,
            demo_mode=demo_mode
        )
        return {
            "model": req.model or os.getenv('OPENAI_MODEL', 'gpt-4o-mini'), 
            "response": text,
            "demo": False
        }
    except RuntimeError as e:
        error_str = str(e)
        # Return 402 for quota errors, 500 for other errors
        status_code = 402 if "quota" in error_str.lower() else 500
        raise HTTPException(status_code=status_code, detail=error_str)


@app.post("/llm/demo", tags=["LLM"])
async def llm_query_demo(req: LLMRequest):
    """Demo LLM endpoint for testing without API quota usage.
    
    This returns a mock response to test the LLM integration without hitting OpenAI API.
    """
    text = call_openai_prompt(
        req.prompt,
        model=req.model,
        max_tokens=req.max_tokens or 256,
        temperature=req.temperature or 0.7,
        demo_mode=True  # Force demo mode
    )
    return {
        "model": req.model or os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
        "response": text,
        "demo": True,
        "note": "This is a demo response. Use /llm endpoint for real API calls."
    }


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*70)
    print("Samsung Smart Phone Advisor - FastAPI Server")
    print("="*70)
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
