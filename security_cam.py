import cv2
import os
import datetime
from ultralytics import YOLO

# Configuration parameters
MODEL_PATH = "yolov8n.pt"  # YOLOv8 model file (pretrained)
RECORDINGS_DIR = "recordings"  # Directory for video recordings
DELETE_OLDER_THAN_DAYS = 30  # Days to keep recordings

# Ensure the recordings directory exists
os.makedirs(RECORDINGS_DIR, exist_ok=True)

# Load YOLOv8 model
model = YOLO(MODEL_PATH)

# Initialize webcam
cap = cv2.VideoCapture(0)

# Set resolution to 1280x720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Variables for video recording
recording = False
out = None
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Video codec and dimensions
fourcc = cv2.VideoWriter_fourcc(*'XVID')
frame_width, frame_height = 1280, 720  # 1280x720 resolution

# Deletes videos older than the specified number of days.
def cleanup_old_videos(directory, days):
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=days)
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_time < cutoff_date:
                os.remove(file_path)

# Starts or continues recording to a video file.
def start_recording(filename):
    return cv2.VideoWriter(filename, fourcc, 20, (frame_width, frame_height))

# Start a new video file for the current day
video_filename = os.path.join(RECORDINGS_DIR, f"{current_date}.avi")
out = start_recording(video_filename)

# Main Loop
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame to 1280x720
        frame = cv2.resize(frame, (frame_width, frame_height))

        # Run YOLOv8 inference
        results = model.predict(frame, conf=0.5, device=0)  # Use GPU (device=0)

        # Filter detections for 'person' class
        person_detected = False
        for r in results:
            if r.boxes.cls.numel() > 0:
                for i in range(len(r.boxes.cls)):
                    if int(r.boxes.cls[i]) == 0:  # Class ID 0 is 'person'
                        person_detected = True
                        box = r.boxes.xyxy[i].cpu().numpy().astype(int)  # Bounding box [x1, y1, x2, y2]
                        confidence = r.boxes.conf[i]  # Confidence score
                        # Draw the bounding box for 'person' only
                        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                        cv2.putText(
                            frame,
                            f"Person {confidence:.2f}",
                            (box[0], box[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 255, 0),
                            2,
                        )

        # Overlay date and time in the bottom-left corner
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(
            frame,
            now,
            (10, frame_height - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

        # Save frame to video file if a person is detected
        if person_detected:
            out.write(frame)

        # Check if the day has changed to start a new file
        new_date = datetime.datetime.now().strftime("%Y-%m-%d")
        if new_date != current_date:
            current_date = new_date
            out.release()  # Close the current video file
            video_filename = os.path.join(RECORDINGS_DIR, f"{current_date}.avi")
            out = start_recording(video_filename)

        # Display the video feed with bounding boxes and time/date
        cv2.imshow("Security Camera", frame)

        # Cleanup old videos daily
        cleanup_old_videos(RECORDINGS_DIR, DELETE_OLDER_THAN_DAYS)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Cleanup resources
    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()
