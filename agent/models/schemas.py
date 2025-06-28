from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ChatRequest(BaseModel):
    message: str
    session_id: str

class AppointmentDetails(BaseModel):
    """Model for calendar event details"""
    start_time: str = Field(..., description="Start time in ISO format")
    end_time: str = Field(..., description="End time in ISO format")
    summary: str = Field("Meeting", description="Event title")
    description: Optional[str] = Field(None, description="Event details")
    location: Optional[str] = Field(None, description="Meeting location")
    attendees: List[str] = Field([], description="List of attendee emails")
    timezone: str = Field("UTC", description="Time zone for the event")

class ChatResponse(BaseModel):
    response: str
    session_id: str
    status: str = "success"