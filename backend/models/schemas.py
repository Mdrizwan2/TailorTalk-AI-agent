from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    session_id: str

class AppointmentDetails(BaseModel):
    start_time: str
    end_time: str
    summary: str = "Meeting"
    attendees: list[str] = []
    timezone: str = "UTC"