from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Samsung Phone Advisor", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to Samsung Phone Advisor API"}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)





















# FASTAPI ENDPOINTS


@app.get("/")
async def root():
    """Health check endpoint"""
    


@app.post("/ask")
async def ask_advisor():
    """
    Main endpoint for Samsung phone advice
    
    """


@app.get("/phones")
async def list_all_phones():
    """Get all available phones in the database"""
    


@app.get("/phones/{model_name}")
async def get_phone_details(model_name: str):
    """Get detailed specs for a specific phone"""
    