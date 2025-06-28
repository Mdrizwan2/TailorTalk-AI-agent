def handle_fallback(state):
    """Handle unrecognized inputs or errors"""
    error_count = state.get("error_count", 0) + 1
    
    if error_count > 2:
        return {
            "response": "I'm having trouble understanding. Please contact support@tailortalk.com for help.",
            "next_step": "end",
            "error_count": error_count
        }
    
    responses = [
        "I didn't quite get that. Could you rephrase?",
        "Sorry, I didn't understand. Try saying something like 'Book a meeting tomorrow at 2pm'",
        "I'm still learning! Try being more specific about the time you want to book."
    ]
    
    return {
        "response": responses[min(error_count - 1, len(responses) - 1)],
        "next_step": "parse_time",
        "error_count": error_count
    }