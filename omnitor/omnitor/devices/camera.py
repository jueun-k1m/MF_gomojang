import os
import cv2
from datetime import datetime
from models import JournalEntry

save_path = JournalEntry.cam_image_path

# Caemera resolution settings
IMAGE_WIDTH = 8000
IMAGE_HEIGHT = 6000
WARM_UP_FRAMES = 30

def decode_fourcc(val):
    return "".join([chr((int(val) >> 8 * i) & 0xFF) for i in range(4)])


def capture_image(save_path: str) -> bool:
    print(f"[{datetime.now()}] Job triggered: Starting picture capture...")
    cap = None
    try:
        os.makedirs(save_path, exist_ok=True)
        filename = f"{datetime.now().strftime('%Y-%m-%d')}.jpg"
        full_path = os.path.join(save_path, filename)
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Cannot open camera. Check connection or other processes.")
            return
            
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        cap.set(cv2.CAP_PROP_FOURCC, fourcc)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMAGE_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMAGE_HEIGHT)
        
        actual_fourcc = decode_fourcc(cap.get(cv2.CAP_PROP_FOURCC))
        actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Requested Format: MJPG, Actual Format: {actual_fourcc}")
        print(f"Requested Resolution: {IMAGE_WIDTH}x{IMAGE_HEIGHT}, Actual Resolution: {actual_width}x{actual_height}")
        
        print(f"Warming up camera for {WARM_UP_FRAMES} frames...")
        for _ in range(WARM_UP_FRAMES):
            cap.read()
        print("Warm-up complete. Capturing final image.")

        ret, frame = cap.read()

        if ret:
            cv2.imwrite(full_path, frame)
            print(f"Success! Picture saved to: {full_path}")
        else:
            print("Error: Failed to capture final image from the camera.")

    except Exception as e:
        print(f"An unexpected error occurred during capture: {e}")
    finally:
        if cap is not None and cap.isOpened():
            cap.release()
            print("Camera resource has been released.")
