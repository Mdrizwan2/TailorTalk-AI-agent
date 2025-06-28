from datetime import datetime, timedelta
import re
from dateutil import parser

def parse_time(state):
    try:
        message = state["message"]
        calendar = state["calendar_service"]
        
        # Parse natural language time
        parsed_time = parser.parse(message, fuzzy=True)
        
        # Find available slots
        start = parsed_time.replace(minute=0)
        end = start + timedelta(hours=1)
        slots = calendar.get_availability(start, end)
        
        if slots:
            return {
                "response": f"I found these available times: {', '.join(slots)}",
                "time_slots": slots,
                "next_step": "confirm"
            }
        
        return {
            "response": "No availability at that time. Try another time?",
            "next_step": "get_time"
        }
    except ValueError:
        return {
            "response": "I couldn't understand that time. Please try again.",
            "next_step": "get_time"
        }