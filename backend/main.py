from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agent.core import BookingAgent
from config.settings import settings
from models.schemas import ChatRequest
from services.calendar import CalendarService

app = FastAPI(title=settings.APP_NAME)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
calendar_service = CalendarService()
agent = BookingAgent(calendar_service)

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint"""
    try:
        response = agent.process(
            message=request.message,
            session_id=request.session_id
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing message: {str(e)}"
        )

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}