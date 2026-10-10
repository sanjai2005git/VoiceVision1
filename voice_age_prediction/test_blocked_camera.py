import os
import cv2
import numpy as np
import customized_testing_phase

def test_blocked_camera():
    temp_dir = os.path.join(os.path.dirname(__file__), "temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    # 1. Generate a solid dark/black image simulating camera blocked
    blocked_img_path = os.path.join(temp_dir, "blocked_camera_test.jpg")
    black_frame = np.zeros((224, 224, 3), dtype=np.uint8)
    cv2.imwrite(blocked_img_path, black_frame)
    
    print("[TEST 1] Testing solid black frame (blocked camera)...")
    res_blocked = customized_testing_phase.predict_face_age(blocked_img_path)
    print("Result for blocked camera:", res_blocked)
    assert res_blocked.get("face_detected") == False, "Expected face_detected to be False for blocked camera"
    assert res_blocked.get("error") == "Face is not recorder", f"Expected 'Face is not recorder', got {res_blocked.get('error')}"
    print("[SUCCESS] Test 1 passed: Camera blockage detected, returned 'Face is not recorder'.")

    # 2. Test valid face if face1.png exists
    face1_path = os.path.join(os.path.dirname(__file__), "face1.png")
    if os.path.exists(face1_path):
        print("\n[TEST 2] Testing normal face image (face1.png)...")
        res_face = customized_testing_phase.predict_face_age(face1_path)
        print("Result for normal face:", res_face.get("success"), res_face.get("overall_class"))

if __name__ == "__main__":
    test_blocked_camera()
