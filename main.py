"""
Samsung Smart Phone Advisor - FastAPI Backend
Multi-Agent System for intelligent phone recommendations and reviews

Agent 1: Data Extractor - Detects phone model and retrieves specs from DB
Agent 2: Review Generator - Generates natural language review using LLM
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re
import os
from dotenv import load_dotenv
from db_setup import fetch_phone_by_model, get_db_connection
import psycopg2

# Load environment variables
load_dotenv()

# Groq API Configuration (FREE - No credit card needed)
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

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


# ============================================================================
# AGENT 1: DATA EXTRACTOR
# ============================================================================

def extract_phone_model(question: str) -> str:
    """
    Agent 1: Extract phone model name from user question
    
    Uses regex patterns to identify Samsung phone models from natural language
    
    Args:
        question: User's question string
    
    Returns:
        Detected phone model name or empty string if not found
    """
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
    """
    Agent 1: Query database for phone specifications
    
    Executes SQL query to retrieve phone data from PostgreSQL
    
    Args:
        model_name: Name of the phone model
    
    Returns:
        Dictionary with phone specifications or None
    """
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


# ============================================================================
# Helper: OpenAI API Caller
# ============================================================================

def call_openai_prompt(prompt: str, model: str | None = None, max_tokens: int = 256, temperature: float = 0.7, demo_mode: bool = False) -> str:
    """
    Call Groq API (FREE - No credit card needed).
    If demo_mode=True, returns mock response for testing.
    
    Groq provides:
    - Completely FREE API access
    - No credit card required
    - Fast inference (10x faster than OpenAI)
    - Quality model: Mixtral 8x7B
    """
    if demo_mode:
        return f"[DEMO MODE] This is a sample LLM response. In production, the model would analyze: '{prompt[:100]}...'"
    
    api_key = GROQ_API_KEY
    if not api_key:
        raise RuntimeError(
            "❌ GROQ_API_KEY is not set.\n\n"
            "📋 To get your FREE API key:\n"
            "1. Go to: https://console.groq.com/keys\n"
            "2. Sign up (completely free, no credit card)\n"
            "3. Create API key (starts with 'gsk_')\n"
            "4. Copy the key and add to .env:\n"
            "   GROQ_API_KEY=gsk_YOUR_KEY_HERE\n"
            "5. Restart the server\n"
            "✅ Done! Your API will work immediately."
        )
    
    try:
        from groq import Groq
        
        client = Groq(api_key=api_key)
        use_model = model or os.getenv('GROQ_MODEL', 'mixtral-8x7b-32768')
        
        response = client.chat.completions.create(
            model=use_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        
        text = response.choices[0].message.content.strip()
        return text
        
    except ImportError:
        raise RuntimeError(
            "❌ Groq library not installed. Run:\n"
            "pip install groq"
        )
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "invalid" in error_msg.lower():
            raise RuntimeError(
                f"❌ Invalid Groq API Key.\n\n"
                f"Please check your key at: https://console.groq.com/keys\n"
                f"Error: {error_msg}"
            )
        else:
            raise RuntimeError(f"❌ Groq API error: {e}")




# ============================================================================
# AGENT 2: REVIEW GENERATOR
# ============================================================================

def call_llm_api(phone_specs: dict, user_question: str) -> str:
    """
    Agent 2: Call LLM to generate natural language review
    
    Sends phone specifications to an LLM (OpenAI or placeholder)
    to generate contextual reviews
    
    Args:
        phone_specs: Dictionary with phone specifications
        user_question: Original user question
    
    Returns:
        Generated review text
    """
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
            
            # Use the centralized OpenAI function that handles errors properly
            review = call_openai_prompt(
                prompt,
                model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
                max_tokens=150,
                temperature=0.7,
                demo_mode=False
            )
            print("[AGENT 2] ✓ Review generated via OpenAI API")
            return review
            
        except ImportError:
            raise RuntimeError("OpenAI package not installed. Run: pip install openai")
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {e}")
    else:
        raise RuntimeError("OPENAI_API_KEY is not set in environment or .env file")


def generate_placeholder_review(phone_specs: dict, user_question: str) -> str:
    """
    Placeholder review generator (when OpenAI API is not available)
    
    Generates contextual reviews based on specs and user question
    
    Args:
        phone_specs: Dictionary with phone specifications
        user_question: Original user question
    
    Returns:
        Generated review text
    """
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


# ============================================================================
# FASTAPI ENDPOINTS
# ============================================================================

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
    """
    Main endpoint for Samsung phone advice
    
    Orchestrates Agent 1 and Agent 2 to provide intelligent recommendations
    
    Flow:
    1. Agent 1 extracts phone model from question
    2. Agent 1 queries database for specs
    3. Agent 2 generates natural language review
    
    Args:
        query: UserQuery object with 'question' field
    
    Returns:
        AdviceResponse with phone model, specs, and generated review
    
    Example:
        POST /ask
        {"question": "Tell me about the Galaxy S24 Ultra"}
    """
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
    
    # AGENT 2: Generate review (only LLM, no fallback)
    try:
        review = call_llm_api(specs, query.question)
    except RuntimeError as e:
        error_msg = str(e)
        if "quota" in error_msg.lower():
            raise HTTPException(
                status_code=402,
                detail=f"OpenAI API quota exceeded. {error_msg}"
            )
        elif "api_key" in error_msg.lower() or "not set" in error_msg.lower():
            raise HTTPException(
                status_code=500,
                detail=f"OpenAI API key not configured. {error_msg}"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"LLM error: {error_msg}"
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


@app.get("/test/openai", tags=["Testing"])
async def test_openai_connection():
    """Test if Groq API connection works and returns detailed diagnostics.
    
    Groq is completely FREE - no credit card needed!
    """
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    groq_key = os.getenv('GROQ_API_KEY')
    
    if not groq_key:
        return {
            "status": "error",
            "message": "❌ GROQ_API_KEY not set",
            "details": "Groq is COMPLETELY FREE - no credit card needed!",
            "next_steps": [
                "📋 STEP 1: Go to https://console.groq.com/keys",
                "📋 STEP 2: Click 'Sign up' (takes 30 seconds)",
                "📋 STEP 3: Verify your email",
                "📋 STEP 4: Click 'Create API Key'",
                "📋 STEP 5: Copy the key (starts with 'gsk_')",
                "📋 STEP 6: Add to .env file:",
                "          GROQ_API_KEY=gsk_YOUR_KEY_HERE",
                "📋 STEP 7: Restart the server",
                "✅ Done! Your API will work immediately"
            ],
            "why_groq": {
                "cost": "FREE forever",
                "credit_card": "NOT required",
                "speed": "10x faster than OpenAI",
                "model": "Mixtral 8x7B (quality)",
                "setup_time": "1 minute"
            }
        }
    
    try:
        from groq import Groq
        client = Groq(api_key=groq_key)
        
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": "Say 'Working!' in one word"}],
            max_tokens=10
        )
        
        return {
            "status": "success",
            "message": "✅ Groq API is working perfectly!",
            "model": "mixtral-8x7b-32768",
            "response": response.choices[0].message.content,
            "key_preview": f"{groq_key[:10]}...",
            "next_steps": ["Your /ask endpoint will now use Groq (FREE)"],
            "info": "Groq is completely free - you can use it for unlimited requests!"
        }
        
    except ImportError:
        return {
            "status": "error",
            "message": "❌ Groq library not installed",
            "next_steps": ["Run: pip install groq"]
        }
        
    except Exception as e:
        error_str = str(e)
        if "401" in error_str:
            return {
                "status": "error",
                "message": "❌ Invalid Groq API Key",
                "key_preview": f"{groq_key[:10]}...",
                "next_steps": [
                    "1. Go to https://console.groq.com/keys",
                    "2. Check if your key is correct",
                    "3. Create a new key if needed",
                    "4. Update .env with the new key",
                    "5. Restart server"
                ]
            }
        else:
            return {
                "status": "error",
                "message": f"❌ Groq API Error: {error_str[:100]}",
                "next_steps": [
                    "Check your internet connection",
                    "Verify API key is correct",
                    "Try creating a new API key at https://console.groq.com/keys"
                ]
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
