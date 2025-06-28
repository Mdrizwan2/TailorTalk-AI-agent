from datetime import datetime, timedelta
from models.schemas import AppointmentDetails

def confirm_booking(state):
    """Handle booking confirmation and create calendar event"""
    message = state["message"].lower()
    calendar = state["calendar_service"]
    
    if "yes" in message or "confirm" in message or "book" in message:
        if not state.get("time_slots"):
            return {
                "response": "No time slot selected. Please specify a time.",
                "next_step": "parse_time"
            }
        
        # Create event details (using first available slot for simplicity)
        slot = state["time_slots"][0]
        start_time = datetime.strptime(slot, "%I:%M %p")
        end_time = start_time + timedelta(minutes=30)
        
        event_details = AppointmentDetails(
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            summary="Scheduled Meeting"
        )
        
        # Create calendar event
        try:
            event = calendar.create_event(event_details.dict())
            return {
                "response": f"Successfully booked your meeting! Here's your calendar link: {event.get('htmlLink')}",
                "next_step": "end"
            }
        except Exception as e:
            return {
                "response": f"Failed to book meeting: {str(e)}",
                "next_step": "fallback"
            }
    
    return {
        "response": "Would you like me to suggest another time?",
        "next_step": "parse_time"
    }