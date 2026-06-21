from project.main_agent import run_agent


def chat() -> None:
    """
    Very simple CLI loop for manual testing.
    """
    print("CrisisInfo Navigator demo. Type 'exit' to quit.")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        response = run_agent(user_input)
        print(f"Agent: {response}")


if __name__ == "__main__":
    chat()
