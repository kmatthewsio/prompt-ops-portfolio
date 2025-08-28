from agents import automotive_agent
from memory import session_manager

def main():
    print("Automotive Agent")
    print("Try: 'What's the price of a 2024 Toyota Camry?'")
    print("Then: 'Calculate payment with $3000 down and 4.5% interest'")
    print("Type 'quit' to exit\n")

    session_id = "demo_session"

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ['quit', 'exit', 'bye']:
            break
        if not user_input:
            continue
        try:
            history = session_manager.get_history(session_id)

            response = automotive_agent.chat(user_input, history)
            ai_message = response["output"]

            print(f"Agent: {ai_message}\n")

            session_manager.add_messages(session_id, user_input, ai_message)

        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()
