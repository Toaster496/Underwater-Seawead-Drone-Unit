import g4f
from g4f.client import Client

# Initialize the GPT client with the desired provider
client = Client()

# Initialize an empty conversation history
messages = []

while True:
    # Get user input
    user_input = input("You: ")

    # Check if the user wants to exit the chat
    if user_input.lower() == "exit":
        print("Exiting chat...")
        break  # Exit the loop to end the conversation

    # Update the conversation history with the user's message
    messages.append({"role": "user", "content": user_input})

    try:
        # Get GPT's response
        response = client.chat.completions.create(
            messages=messages,
            model="gpt-4o",
            provider="Airforce"
        )

        # Extract the GPT response and print it
        gpt_response = response.choices[0].message.content
        print(f"Bot: {gpt_response}")

        # Update the conversation history with GPT's response
        messages.append({"role": "assistant", "content": gpt_response})

    except Exception as e:
        print(f"An error occurred: {e}")