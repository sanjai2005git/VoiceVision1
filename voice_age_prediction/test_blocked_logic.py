import os
import cv2
import numpy as np
import customized_testing_phase

def test_blocked_detection():
    temp_dir = os.path.join(os.path.dirname(__file__), "temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Generate a solid black frame simulating camera blocked
    blocked_img_path = os.path.join(temp_dir, "blocked_camera_quick.jpg")
    black_frame = np.zeros((224, 224, 3), dtype=np.uint8)
    cv2.imwrite(blocked_img_path, black_frame)
    
    print("[TEST] Running detect_faces on blocked camera frame...")
    img, boxes = customized_testing_phase.detect_faces(blocked_img_path, 2)
    print("Boxes returned:", boxes)
    assert len(boxes) == 0, f"Expected 0 boxes for blocked camera, got {len(boxes)}"
    
    print("[TEST] Running predict_face_age on blocked camera frame...")
    result = customized_testing_phase.predict_face_age(blocked_img_path)
    print("Result dictionary:", result)
    assert result.get("face_detected") == False, "Expected face_detected == False"
    assert result.get("error") == "Face is not recorder", f"Expected 'Face is not recorder', got {result.get('error')}"
    print("\n[ALL TESTS PASSED SUCCESSFULLY!]")

if __name__ == "__main__":
    test_blocked_detection()
