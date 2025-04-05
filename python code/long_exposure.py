import cv2
import numpy as np
import time
import os

def long_exposure(camera_index=0, num_frames=10, delay_seconds=0.1, output_path="long_exposure.jpg"):
    """
    Captures multiple frames from a camera and averages them to simulate a long exposure.

    Args:
        camera_index (int): The index of the camera to use (usually 0 for the default webcam).
        num_frames (int): The number of frames to capture and average. Higher values simulate longer exposures.
        delay_seconds (float): The delay in seconds between capturing each frame.
        output_path (str): The path to save the resulting long exposure image.
    """
    try:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            raise IOError(f"Cannot open webcam with index {camera_index}")

        ret, frame = cap.read()
        if not ret:
            raise IOError("Failed to read the first frame.")

        accumulated_frame = np.float32(frame)

        print(f"Capturing {num_frames} frames for long exposure...")
        for i in range(num_frames - 1):
            time.sleep(delay_seconds)
            ret, frame = cap.read()
            if not ret:
                print(f"Warning: Failed to read frame {i+2}. Continuing with accumulated data.")
                continue
            cv2.accumulateWeighted(frame, accumulated_frame, 1 / (i + 2))
            print(f"Captured frame {i+2}/{num_frames}")

        final_frame = np.uint8(accumulated_frame)
        cv2.imwrite(output_path, final_frame)
        print(f"Long exposure image saved to: {output_path}")

    except IOError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if 'cap' in locals() and cap.isOpened():
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    # --- Configuration ---
    camera_id = 0  # Change this if you have multiple cameras
    number_of_frames = 30  # Increase for longer simulated exposure
    capture_delay = 0.05 # Adjust the delay between frames
    output_file = "long_exposure_result.jpg"

    # --- Run the long exposure function ---
    long_exposure(camera_index=camera_id,
                  num_frames=number_of_frames,
                  delay_seconds=capture_delay,
                  output_path=output_file)