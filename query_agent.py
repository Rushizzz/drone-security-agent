import chromadb
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# connect to existing memmory
client = chromadb.PersistentClient(path="./drone_db")
collection = client.get_or_create_collection(name="drone_logs")

# initialize the LLM
llm = OllamaLLM(model="llama3.2")

# define security analyst personality
template = """
You are a Drone Security Analyst. Use the security logs and the previous conversation history to answer.

Security Logs:
{context}

Conversation History:
{chat_history}

Current Question: {question}
Answer:"""

prompt = ChatPromptTemplate.from_template(template)

# initialize empty conversation history
chat_history = []

def ask_agent(user_query):
    # 1. Search the database for the 3 most similar logs
    results = collection.query(
        query_texts=[user_query],
        n_results=3
    )
    context_logs = "\n".join(results['documents'][0])

    history_str = "\n".join(chat_history)

    # generate response
    final_prompt = prompt.format(
        context=context_logs,
        chat_history=history_str, 
        question=user_query
    )
    response = llm.invoke(final_prompt)
    
    # update chat history
    chat_history.append(f"User: {user_query}")
    chat_history.append(f"Analyst: {response}")

    return response

# if __name__ == "__main__":
#     print("Welcome to the Drone Security Analyst Agent!")
#     print("Type 'exit' to quit.")

#     while True:
#         user_input = input("\n [Analyst Query] : ")

#         if user_input.lower() in ["exit", "quit", "q"]:
#             print("Closing connetion to drone memory")
#             break

#         if user_input.strip() == "":
#             print("Please enter a valid query.")
#             continue

#         # Call the agent with the user's query
#         answer = ask_agent(user_input)
#         print(f"\n [Agent Response] : {answer}")     
