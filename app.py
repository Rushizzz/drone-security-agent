from main_agent import run_pipeline
from query_agent import ask_agent

if __name__ == "__main__":
    
    run_pipeline()

    print("Welcome to the Drone Security Analyst Agent!")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\n [Analyst Query] : ")

        if user_input.lower() in ["exit", "quit", "q"]:
            print("Closing connetion to drone memory")
            break

        if user_input.strip() == "":
            print("Please enter a valid query.")
            continue

        # Call the agent with the user's query
        answer = ask_agent(user_input)
        print(f"\n [Agent Response] : {answer}")     
