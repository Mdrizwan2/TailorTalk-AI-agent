from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from config.settings import settings
from typing import List

class CalendarService:
    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_info(
            settings.GOOGLE_SERVICE_ACCOUNT,
            scopes=['https://www.googleapis.com/auth/calendar']
        )
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def get_availability(self, start_time: datetime, end_time: datetime) -> List[str]:
        """Get available time slots between two datetimes"""
        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=start_time.isoformat() + 'Z',
            timeMax=end_time.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        busy_slots = events_result.get('items', [])
        return self._find_available_slots(start_time, end_time, busy_slots)

    def _find_available_slots(self, start, end, busy_slots):
        """Generate available 30-minute slots between busy periods"""
        slots = []
        current = start
        
        while current < end:
            slot_end = current + timedelta(minutes=30)
            available = True
            
            for event in busy_slots:
                event_start = datetime.fromisoformat(event['start'].get('dateTime'))
                event_end = datetime.fromisoformat(event['end'].get('dateTime'))
                
                if not (slot_end <= event_start or current >= event_end):
                    available = False
                    break
            
            if available:
                slots.append(current.strftime("%I:%M %p"))
            
            current += timedelta(minutes=30)
        
        return slots

    def create_event(self, event_details: dict):
        """Create a new calendar event"""
        event = self.service.events().insert(
            calendarId='primary',
            body=event_details
        ).execute()
        return event