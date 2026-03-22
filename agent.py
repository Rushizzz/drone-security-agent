import json
import time
from datetime import datetime
import chromadb
from chromadb.utils import embedding_functions

# local vector DB
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="drone_frames")
sentence_transformers_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

def check_security_rules(frame):
    # Predefined rules for real time alerts 
    description = frame["frame_description"].lower()
    timestamp = datetime.fromisoformat(frame["timestamp"])
    hour = timestamp.hour

    alerts = []

    # Rule 1: Loitering at night
    if (hour >= 22 or hour <=5 ) and "person" in description:
        alerts.append(f"ALERT: Person loitering at {frame['telemetry']['location']} at {frame['timestamp']}!")
    
    # Rule 2: Specific vehicle tracking
    if "blue ford f150" in description:
        alerts.append(f"LOG: Target vehicle (Blue Ford F150) detected at {frame['telemetry']['location']}.")

    return alerts

def index_frame(frame):
    # Store frame in DB for future querying
    collection.add(
        documents=[frame['frame_description']],
        metadatas=[{
            "location": frame['telemetry']['location'],
            "time": frame['timestamp']
        }],
        ids=[str(frame['frame_id'])]
    )

def run_drone_analyst():
    with open('simulation_data.json', 'r') as f:
        data = json.load(f)

    print("--- Drone Security Agent Active ---")
    for frame in data:
        print(f"\n[Frame {frame['frame_id']}] Scanning...")

        # Real time analysis
        alerts = check_security_rules(frame)
        for alert in alerts:
            print(f" >> {alert}")

        # Index for future
        index_frame(frame)
        time.sleep(1)  # Simulate real-time processing delay

    # Demonstrate querying
    print("\n--- Testing Index Query: 'Show all truck events' ---")
    results = collection.query(
        query_texts=["truck"],
        n_results=2
    )
    print(f"Search Results: {results['documents']}")

if __name__ == "__main__":
    run_drone_analyst()