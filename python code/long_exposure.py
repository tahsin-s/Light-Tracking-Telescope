import cv2
import numpy as np
import time
import os

def amplify_light_long_exposure(camera_index=0, num_frames=30, delay_seconds=0.1, output_path="deep_space.jpg", gain=2.0):
    """
    Captures multiple frames and averages them to simulate a long exposure,
    with a basic amplification step to enhance faint details.

    Warning: This script alone is NOT a substitute for proper astrophotography techniques
             like tracking mounts, dark/flat frame calibration, and specialized cameras.
             It's a basic demonstration of light accumulation.

    Args:
        camera_index (int): The index of the camera to use.
        num_frames (int): The number of frames to capture and average.
        delay_seconds (float): The delay in seconds between capturing each frame.
        output_path (str): The path to save the resulting image.
        gain (float): A multiplicative factor to amplify the pixel values after averaging.
                      Values greater than 1.0 will brighten the image. Use with caution
                      as it can also amplify noise.
    """
    try:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            raise IOError(f"Cannot open webcam with index {camera_index}")

        ret, frame = cap.read()
        if not ret:
            raise IOError("Failed to read the first frame.")

        accumulated_frame = np.float32(frame)

        print(f"Capturing {num_frames} frames for light accumulation...")
        for i in range(num_frames - 1):
            time.sleep(delay_seconds)
            ret, frame = cap.read()
            if not ret:
                print(f"Warning: Failed to read frame {i+2}. Continuing with accumulated data.")
                continue
            cv2.accumulateWeighted(frame, accumulated_frame, 1 / (i + 2))
            print(f"Captured frame {i+2}/{num_frames}")

        averaged_frame = accumulated_frame

        # Basic amplification (can also amplify noise)
        amplified_frame = np.clip(averaged_frame * gain, 0, 255)
        final_frame = np.uint8(amplified_frame)

        cv2.imwrite(output_path, final_frame)
        print(f"Light-amplified image saved to: {output_path}")

    except IOError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if 'cap' in locals() and cap.isOpened():
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    # --- Configuration for attempting deep space (adjust carefully) ---
    camera_id = 1
    number_of_frames = 100  # Try a higher number of frames
    capture_delay = 0.05
    output_file = "deep_space_attempt.jpg"
    amplification_factor = 3.0  # Experiment with this value

    print("Warning: Capturing deep space objects with a standard webcam is challenging.")
    print("Consider using a dark location with minimal light pollution and a stable setup.")

    amplify_light_long_exposure(camera_index=camera_id,
                  num_frames=number_of_frames,
                  delay_seconds=capture_delay,
                  output_path=output_file,
                  gain=amplification_factor)