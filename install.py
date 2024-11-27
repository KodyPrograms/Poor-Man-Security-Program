import os
import subprocess

# Install required Python packages
def install_dependencies():
    print("Installing dependencies...")
    subprocess.check_call(["pip", "install", "--upgrade", "pip"])
    packages = [
        "opencv-python",
        "opencv-python-headless",
        "ultralytics",
    ]
    for package in packages:
        subprocess.check_call(["pip", "install", package])

# Download YOLOv8 model
def download_yolo_model(model_path="yolov8n.pt"):
    if not os.path.exists(model_path):
        print(f"Downloading YOLOv8 model to {model_path}...")
        url = "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
        subprocess.check_call(["curl", "-L", "-o", model_path, url])
    else:
        print(f"YOLOv8 model already exists at {model_path}.")

if __name__ == "__main__":
    install_dependencies()
    download_yolo_model()
    print("Setup complete. You can now run `python security_camera.py`.")
