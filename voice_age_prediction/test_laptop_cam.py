import os
import customized_testing_phase

def test_laptop_camera():
    print("[TEST] Testing OpenCV laptop camera capture...")
    cam_output = customized_testing_phase.capture_from_laptop_camera("temp/test_laptop_cam.jpg")
    if cam_output and os.path.exists(cam_output):
        print(f"[SUCCESS] Laptop camera captured image successfully at {cam_output}")
        result = customized_testing_phase.predict_face_age(cam_output)
        print("Prediction result on laptop camera capture:", result.get("success"), result.get("overall_class") or result.get("error"))
    else:
        print("[INFO] No hardware camera accessible or camera was unavailable in headless environment.")

if __name__ == "__main__":
    test_laptop_camera()
