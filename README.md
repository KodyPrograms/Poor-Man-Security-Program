# Poor Man Security Program

This project implements a basic webcam using the YOLOv8 object detection model to detect and record videos of people in real time. The application saves daily recordings, and old recordings are automatically deleted after a specified number of days.

## Features
- Real-time person detection using YOLOv8.
- Saves video recordings only when a person is detected.
- Automatically deletes recordings older than a configurable number of days.
- Displays live video feed with bounding boxes for detected persons.
- Includes date and time overlay on the video feed.

## Requirements
- Python 3.7+
- Webcam or camera device.
- Pre-trained YOLOv8 model.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/KodyPrograms/Poor-Man-Security-Program.git
   cd Poor-Man-Security-Program
   ```

2. Install dependencies:
   ```bash
   python install.py
   ```

3. Ensure the YOLOv8 model is downloaded to the project directory (`yolov8n.pt` by default).

## Usage
Run the application:
```bash
python security_camera.py
```

## Configuration
- `MODEL_PATH`: Path to the YOLOv8 model file.
- `RECORDINGS_DIR`: Directory to save video recordings.
- `DELETE_OLDER_THAN_DAYS`: Number of days to retain old recordings.
- `frame_width` and `frame_height`: Video resolution settings. 720p by default.

## Controls
- Press `q` to quit the application.

## License
This project utilizes other dependencies such as Ultralytics YOLO and require them to function.
