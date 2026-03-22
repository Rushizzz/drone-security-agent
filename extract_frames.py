import cv2
import os

def extract_frames(video_path, output_folder, interval_seconds=45):
    # create output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Load the video
    cam = cv2.VideoCapture(video_path)
    fps = cam.get(cv2.CAP_PROP_FPS)

    # Calculate the interval in terms of frames
    frame_interval = int(fps * interval_seconds)

    current_frame = 0
    saved_count = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        if current_frame % frame_interval == 0:
            name = os.path.join(output_folder, f"frame_{saved_count}.jpg")
            cv2.imwrite(name, frame)
            print(f"Captured: {name}")
            saved_count += 1
        
        current_frame += 1
    cam.release()
    print(f"Done! Extracted {saved_count} frames.")

if __name__ == "__main__":
    extract_frames("drone-footage.mp4", "extracted_frames", 1)
