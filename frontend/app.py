import streamlit as st
import requests
from datetime import datetime

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d%H%M%S")

# API configuration
BACKEND_URL = "http://localhost:8000/api"

def send_message(message: str) -> str:
    """Send user message to backend and get response"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={
                "message": message,
                "session_id": st.session_state.session_id
            }
        )
        return response.json().get("response", "Sorry, I didn't understand that.")
    except requests.exceptions.RequestException:
        return "Connection to server failed. Please try again later."

def render_chat():
    """Display chat interface and handle interactions"""
    st.title("📅 TailorTalk Booking Assistant")
    st.caption("A conversational AI for scheduling meetings")

    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Handle user input
    if prompt := st.chat_input("When would you like to schedule?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Get and display assistant response
        response = send_message(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

if __name__ == "__main__":
    render_chat()