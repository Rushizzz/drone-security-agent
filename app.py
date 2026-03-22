import gc
import torch
import vision_engine  # We import this to access the model/processor directly
from main_agent import run_pipeline
from query_agent import ask_agent

if __name__ == "__main__":
    # --- PHASE 1: INGESTION ---
    print("Starting Video Ingestion Phase...")
    run_pipeline()

    # --- MEMORY RELEASE PHASE ---
    print("\nIngestion complete. Releasing VRAM for the Query Agent...")
    
    # 1. Delete the heavy objects from memory
    # We access them through the vision_engine module where they were defined
    if hasattr(vision_engine, 'model'):
        del vision_engine.model
    if hasattr(vision_engine, 'processor'):
        del vision_engine.processor

    # 2. Force Python to clear unused variables
    gc.collect()

    # 3. Tell CUDA to actually free up the VRAM "parking spots"
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
    
    print("VRAM Cleared. Ready for Llama 3.2.\n")

    # --- PHASE 2: INTERACTION ---
    print("Welcome to the Drone Security Analyst Agent!")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\n [Analyst Query] : ")

        if user_input.lower() in ["exit", "quit", "q"]:
            print("Closing connection to drone memory...")
            break

        if user_input.strip() == "":
            print("Please enter a valid query.")
            continue

        # Call the agent with the user's query
        answer = ask_agent(user_input)
        print(f"\n [Agent Response] : {answer}")