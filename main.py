import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from db_setup import fetch_all_phones_full_data, fetch_phone_by_model

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')

app = FastAPI(title="Samsung Advisor Pro", version="3.0.0")

class UserQuery(BaseModel):
    question: str

# --- RAG Logic: Send All Data to AI ---
def get_ai_response(user_question):
    all_data = fetch_all_phones_full_data()
    
    db_context = "Samsung Phone Database:\n"
    for p in all_data:
        db_context += f"- {p['model']}: {p['price']}, Display: {p['display']}, Camera: {p['camera']}, Battery: {p['battery']}, Colors: {p['color']}\n"

    prompt = f"""
    You are a smart Samsung Assistant. Use the following database to answer the user's question.
    If the user asks for a comparison, price filter, or recommendation, analyze the data and give a humanized answer.

    DATABASE:
    {db_context}

    USER QUESTION: "{user_question}". Give and only based on USER QUESTION.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"AI Error: {str(e)}"


# ALL API ROUTES


@app.get("/")
def root():
    return {"status": "Online", "mode": "Level-1 RAG"}

# Route 1: Get all phones (List)
@app.get("/phones", tags=["Database"])
def list_phones():
    data = fetch_all_phones_full_data()
    return {"count": len(data), "phones": [{"model": x['model'], "price": x['price']} for x in data]}

# Route 2: Get specific phone details
@app.get("/phones/{model_name}", tags=["Database"])
def phone_details(model_name: str):
    specs = fetch_phone_by_model(model_name)
    if not specs: raise HTTPException(status_code=404, detail="Phone not found")
    return {"specs": specs}

# Route 3: Smart AI Advisor (The RAG Endpoint)
@app.post("/ask", tags=["AI Agent"])
async def ask_advisor(query: UserQuery):
    answer = get_ai_response(query.question)
    return {"answer": answer}