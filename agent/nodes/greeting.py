def greet_user(state):
    message = state["message"].lower()
    
    greetings = ["hi", "hello", "hey", "greetings"]
    if any(greet in message for greet in greetings):
        return {
            "response": "Hello! I can help you schedule meetings. When would you like to book?",
            "next_step": "get_time"
        }
    
    return {
        "response": "When would you like to schedule?",
        "next_step": "get_time"
    }