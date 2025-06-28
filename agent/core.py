from langgraph.graph import Graph, END
from nodes.greeting import greet_user
from nodes.time_parsing import parse_time
from nodes.confirmation import confirm_booking
from nodes.fallback import handle_fallback
from models.schemas import AppointmentDetails

class BookingAgent:
    def __init__(self, calendar_service):
        self.calendar = calendar_service
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        workflow = Graph()
        
        # Define nodes
        workflow.add_node("greet", greet_user)
        workflow.add_node("parse_time", parse_time)
        workflow.add_node("confirm", confirm_booking)
        workflow.add_node("fallback", handle_fallback)
        
        # Define edges
        workflow.add_edge("greet", "parse_time")
        workflow.add_conditional_edges(
            "parse_time",
            self._decide_next_step,
            {
                "confirm": "confirm",
                "fallback": "fallback"
            }
        )
        workflow.add_edge("confirm", END)
        workflow.add_edge("fallback", END)
        
        workflow.set_entry_point("greet")
        return workflow

    def _decide_next_step(self, state):
        if state.get("time_slots"):
            return "confirm"
        return "fallback"

    def process(self, message: str, session_id: str):
        result = self.workflow.run({
            "message": message,
            "session_id": session_id,
            "calendar_service": self.calendar
        })
        return result.get("response", "I couldn't process that request.")