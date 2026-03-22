import json 
import time
from datetime import datetime
import chromadb
from vision_engine import get_vlm_description

# setup chromadb for indexing
client = chromadb.PersistentClient(path="./drone_db")
collection = client.get_or_create_collection(name="drone_logs")

def analyze_and_alert(frame_data, description):
    timestamp = datetime.fromisoformat(frame_data['timestamp'])
    hour = timestamp.hour
    desc_lower =description.lower()

    alerts = []

    if "blue" in desc_lower and "truck" in desc_lower:
        alerts.append(f"LOG: Blue Ford F150 identified at {frame_data['location']}.")

    if (hour >= 22 or hour <= 4) and ("man" in desc_lower or "person" in desc_lower):
        alerts.append(f"ALERT: Person loitering at {frame_data['location']} at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}.")

    return alerts

def run_pipeline():
    with open("simulation_data.json", "r") as f:
        simulation_steps = json.load(f)
    
    for step in simulation_steps:
        print(f"\n--- Processing Frame {step['frame_id']} ---")

        # VLM Generation
        description = get_vlm_description(step['image'])
        print(f"VLM Analysis: {description}")

        # Rule Based Alerting
        alerts = analyze_and_alert(step, description)
        for alert in alerts:
            print(f"activity detected: {alert}")

        # indexing for search
        collection.add(
            documents=[description],
            metadatas=[{"time": step['timestamp'], "loc": step['location']}],
            ids=[str(step['frame_id'])]
        )
        time.sleep(1)  # simulate processing time

if __name__ == "__main__":
    run_pipeline()