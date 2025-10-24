import os
import sys
import openai

# Fetch the OpenAI API key from environment variables
open_api_key = os.getenv('OPENAI_API_KEY')  # Ensure you set the OPENAI_API_KEY in your environment

# Check the key
if not open_api_key:
    print("No API key was found")
    sys.exit("Error: The OPENAI_API_KEY environment variable is not set.")
elif not open_api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start with sk-proj-; please check you're using the right key")
elif open_api_key.strip() != open_api_key:
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them ")
else:
    print(f"✅ API key found and looks good so far! Begins with {open_api_key[:8]}")

# Set the OpenAI API key
openai.api_key = open_api_key

MODEL = "gpt-4o-mini"  # or 'gpt-4o-mini'
TEMPERATURE = 0.5
MAX_TOKENS = 400

# Define the system prompt for the chatbot
SYSTEM_PROMPT = """Role:
Act like an expert local tourism guide, who takes the number of people, the date, and the interests of travelers and then makes a suitable plan for them. You have updated information about the new places or events in your city. After each recommendation, evaluate the feedback from travelers and adjust it into the plan. Always respond with plans and schedules with the least text to make the journey enjoyable.

Task:
Begin with a short questionnaire to know the interests of the traveler.
Start making the plan with a focus on dates and other limitations.
Provide the response in a simple formatted schedule.

Context:
The users are travelers who don't know much about the city.
They need a plan that matches their interest and status.
Keep tone conversational, exploratory, and adjusting.
Always provide multiple solutions for the plan.

Reasoning:
Before answering, outline your internal reasoning:
- What is the interest of the traveler?
- What’s the simplest way to order the plan?
- Which special or new events are in the city?

Output Format:
Return your final answer in this structure:
### About the city
[Explain simply]

### Overview of the schedule and plan
[In brief, what are the places and duration?]

### Whole plan or schedule
[Full plan]

### Any notes or considerations
[2–3 bullet points]

Stop Conditions:
Stop once the response covers the concept, its duration, and its most famous city.
Do not generate extra guidance or unrelated recommendations.
End when the traveler could re-ask the plan in their own words.
"""

# Build messages to send to OpenAI API
def build_messages(history, user_input):
    return (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + history
        + [{"role": "user", "content": user_input}]
    )


# Get the reply from OpenAI based on the user's input and history
def get_guide_assistant_reply(history, user_input):
    messages = build_messages(history, user_input)
    try:
        response = openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
        return response.choices[0].message.content.strip()
    except Exception as err:
        return f"⚠️ API Error: {err}"


# Function to handle user input, chat history, and generate response
def respond(user_input, chat_history, message_history):
    chat_history = chat_history or []
    message_history = message_history or []

    # Get assistant's reply
    reply = get_guide_assistant_reply(message_history, user_input)

    # Update histories
    message_history.extend([
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": reply}
    ])
    chat_history.append((user_input, reply))

    # Return updated history and response
    return chat_history, message_history, reply


# Start the terminal-based interface
def run_chatbot():
    print("Welcome to the local city guide chatbot! 🌍")
    print("Please provide your travel details (e.g., number of people, date, interests).")

    chat_history = []
    message_history = []

    while True:
        # Get user input
        user_input = input("\nEnter your travel details or type 'exit' to quit: ")
        
        if user_input.lower() == 'exit':
            print("Thank you for using the Travel Guide Bot! Have a great trip! ✈️")
            break

        # Get the assistant's response
        chat_history, message_history, reply = respond(user_input, chat_history, message_history)
        
        # Display the assistant's response
        print("\nAssistant's Plan:")
        print(reply)


# Run the chatbot
if __name__ == "__main__":
    run_chatbot()
