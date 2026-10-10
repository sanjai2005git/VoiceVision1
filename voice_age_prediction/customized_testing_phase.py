# -*- coding: utf-8 -*-
"""
Customized Testing Phase: Face Detection & Age Prediction Pipeline
"""

import os
import re
import cv2
import json
import glob
import joblib
import urllib.request
import numpy as np
import tensorflow as tf
from datetime import datetime
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Suppress TensorFlow GPU/CPU logs and warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')

# Dynamic imports for optional/conditional face detectors
try:
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
except ImportError:
    mp = None

try:
    from mtcnn import MTCNN
except ImportError:
    MTCNN = None

# =====================================================================
# 1. CONFIGURATION BLOCK (Single Place to Edit)
# =====================================================================
Model_Selection = 2  # 1 = MediaPipe, 2 = OpenCV Haar Cascade, 3 = MTCNN
Preprocessing = False
Preprocessing_Steps = ['resize', 'lighting/contrast normalization', 'noise reduction', 'pixel normalization']
NeedCNN = True       # If False, use MediaPipe-landmark NN
MediaPipe_LandMark_NN = 0
ConvNextTiny_Select = 0
bin_Selected = 0      # Index into bins_Available
bins_Available = [10, 3, 6]

Paths = {
    "mediapipe_task_url": "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task",
    "mediapipe_task_local": "face_landmarker.task",
    "mediapipe_nn_models": [
        "/content/drive/MyDrive/Deep_learning_project/Parental_Control_project/Sanjay_Upload/Age_Recognition/Models/best_indface_categorical_model.keras",
        "/content/drive/MyDrive/Deep_learning_project/Parental_Control_project/Sanjay_Upload/Age_Recognition/Models/2-indface-22-07-2026_08-16-55_597.keras",
        "/content/drive/MyDrive/Deep_learning_project/Parental_Control_project/Sanjay_Upload/Age_Recognition/Models/1-indface-22-07-2026_08-11-17_172.keras",
        "/content/drive/MyDrive/Deep_learning_project/Parental_Control_project/Sanjay_Upload/Age_Recognition/Models/3-indface-22-07-2026_08-33-32.keras",
        "/content/drive/MyDrive/Deep_learning_project/Parental_Control_project/Sanjay_Upload/Age_Recognition/Models/5-indface-22-07-2026_09-36-07.keras",
        "/content/drive/MyDrive/Deep_learning_project/Parental_Control_project/Sanjay_Upload/Age_Recognition/Models/indface_20260722_094646.keras"
    ],
    "mediapipe_scaler": "/content/drive/MyDrive/Deep_learning_project/Parental_Control_project/Sanjay_Upload/Age_Recognition/Models/scaler.pkl",
    "convnext_models": {
        10: [
            "/content/drive/MyDrive/Deep_learning_project/Parental_Control_project/Sanjay_Upload/Age_Recognition/CNN-Models/ConvNeXt_Tiny_Age_10Bins_2026-07-27_06-15-29.keras",
            "/content/drive/MyDrive/Deep_learning_project/Parental_Control_project/Sanjay_Upload/Age_Recognition/CNN-Models/ConvNeXt_Tiny_Age_10Bins_2026-07-27_07-11-42.keras"
        ],
        3: [
            "/content/drive/MyDrive/Deep_learning_project/Parental_Control_project/Sanjay_Upload/Age_Recognition/CNN-Models/3_ConvNext_Tiny_Age_3Bins_2026-07-28_05-47-46.keras",
            "/content/drive/MyDrive/Deep_learning_project/Parental_Control_project/Sanjay_Upload/Age_Recognition/CNN-Models/4_ConvNext_Tiny_Age_3Bins_2026-07-28_06-11-28.keras"
        ],
        6: [
            "/content/drive/MyDrive/Deep_learning_project/Parental_Control_project/Sanjay_Upload/Age_Recognition/CNN-Models/5_ConvNext_Tiny_Age_6Bins_2026-07-28_06-36-54.keras"
        ]
    },
    "convnext_scaler": "/content/drive/MyDrive/Deep_learning_project/Parental_Control_project/Sanjay_Upload/Age_Recognition/CNN-Models/Scalar/dataset_metadata.pkl"
}

IO = {
    "input_image_path": "/content/drive/MyDrive/Deep_learning_project/Parental_Control_project/Sanjay_Upload/Age_Recognition/UTKFace/7_1_3_20161220221712842.jpg.chip.jpg",
    "temp_face_dir": "/content/temp_faces",
    "results_log": "/content/drive/MyDrive/Deep_learning_project/Parental_Control_project/Logs"
}

# =====================================================================
# 2. DYNAMIC PATH MAPPING (Colab / Local Workspace Resolver)
# =====================================================================
def resolve_path(path):
    """Dynamically resolves Google Drive/Colab path patterns to local folder structure."""
    if not path:
        return path
    
    path = path.replace("\\", "/")
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local_age_rec_root = os.path.join(workspace_root, "Age_Recognition-20260828T133809Z-1-001", "Age_Recognition")
    
    gdrive_prefix = "/content/drive/MyDrive/Deep_learning_project/Parental_Control_project/Sanjay_Upload/Age_Recognition"
    colab_local_prefix = "/content"
    
    if path.startswith(gdrive_prefix):
        rel_path = os.path.relpath(path, gdrive_prefix)
        return os.path.abspath(os.path.join(local_age_rec_root, rel_path))
    elif path.startswith(colab_local_prefix):
        rel_path = os.path.relpath(path, colab_local_prefix)
        # Store in local voice_age_prediction directory
        return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), rel_path))
        
    return os.path.abspath(path)

# =====================================================================
# 3. CONVERT AND RETRIEVE DOCK DETAILS
# =====================================================================
def download_mediapipe_task(url, local_path):
    """Downloads official MediaPipe FaceLandmarker model file if missing."""
    resolved_local = resolve_path(local_path)
    if not os.path.exists(resolved_local):
        print(f"[INFO] Downloading MediaPipe FaceLandmarker task from {url}...")
        os.makedirs(os.path.dirname(resolved_local), exist_ok=True)
        urllib.request.urlretrieve(url, resolved_local)
        print("[INFO] Download completed.")
    return resolved_local

# =====================================================================
# 4. CONTRAST ENHANCEMENT FOR RETRIES
# =====================================================================
def apply_clahe(img):
    """Applies CLAHE on luminance channel of LAB to improve features before retry."""
    if len(img.shape) == 3 and img.shape[2] == 3:
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l_eq = clahe.apply(l)
        return cv2.cvtColor(cv2.merge((l_eq, a, b)), cv2.COLOR_LAB2BGR)
    else:
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        return clahe.apply(img)

# =====================================================================
# 5. FACE DETECTION WITH FALLBACKS
# =====================================================================
def _run_single_detector(image, choice):
    """Runs a single detector choice and returns bounding boxes [(x, y, w, h), ...]"""
    boxes = []
    
    if choice == 1:  # MediaPipe Vision Tasks
        if mp is None:
            raise ImportError("MediaPipe package is not installed.")
        task_path = download_mediapipe_task(Paths["mediapipe_task_url"], Paths["mediapipe_task_local"])
        base_options = python.BaseOptions(model_asset_path=task_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False,
            num_faces=5
        )
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        
        with vision.FaceLandmarker.create_from_options(options) as landmarker:
            res = landmarker.detect(mp_image)
            h, w, _ = image.shape
            if res.face_landmarks:
                for landmarks in res.face_landmarks:
                    xs = [lm.x * w for lm in landmarks]
                    ys = [lm.y * h for lm in landmarks]
                    xmin, xmax = int(min(xs)), int(max(xs))
                    ymin, ymax = int(min(ys)), int(max(ys))
                    boxes.append((xmin, ymin, xmax - xmin, ymax - ymin))
                    
    elif choice == 2:  # Haar Cascade
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        detected = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        boxes = [(x, y, w, h) for (x, y, w, h) in detected]
        
    elif choice == 3:  # MTCNN
        if MTCNN is None:
            raise ImportError("MTCNN package not installed.")
        detector = MTCNN()
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = detector.detect_faces(rgb_image)
        boxes = [res['box'] for res in results if res['confidence'] > 0.8]
        
    return boxes

def capture_from_laptop_camera(output_path="temp/laptop_cam_capture.jpg"):
    """Captures a single frame from the laptop camera using OpenCV."""
    resolved_output = resolve_path(output_path)
    os.makedirs(os.path.dirname(os.path.abspath(resolved_output)), exist_ok=True)
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Could not open laptop camera.")
        return None
        
    ret, frame = cap.read()
    cap.release()
    
    if not ret or frame is None:
        print("[ERROR] Failed to grab frame from laptop camera.")
        return None
        
    cv2.imwrite(resolved_output, frame)
    print(f"[SUCCESS] Captured frame from laptop camera saved to: {resolved_output}")
    return resolved_output

def detect_faces(image_path, primary_choice):
    """Detects faces using fallbacks, contrast retries, and clamps coordinates."""
    resolved_path = resolve_path(image_path)
    image = cv2.imread(resolved_path)
    if image is None:
        raise FileNotFoundError(f"Could not load image from: {resolved_path}")
        
    h, w, _ = image.shape
    boxes = []
    
    # Check if image is dark or blocked (e.g. camera covered)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if np.mean(gray) < 15 or np.std(gray) < 10:
        print("[INFO] Camera appears to be blocked or frame is obscured.")
        return image, []

    # 1. Primary detector attempt
    try:
        boxes = _run_single_detector(image, primary_choice)
    except Exception as e:
        print(f"[WARNING] Primary detector ({primary_choice}) failed: {e}")
        
    # 2. If no faces, apply CLAHE contrast enhancement & retry primary detector
    if not boxes:
        print("[INFO] Face not found. Applying contrast enhancement (CLAHE) and retrying primary detector...")
        enhanced = apply_clahe(image)
        try:
            boxes = _run_single_detector(enhanced, primary_choice)
        except Exception:
            pass
            
    # 3. Alternate detector fallbacks sequence
    if not boxes:
        detectors_fallback = [2, 3, 1]  # Cascade -> MTCNN -> MediaPipe
        if primary_choice in detectors_fallback:
            detectors_fallback.remove(primary_choice)
        
        for alternate in detectors_fallback:
            print(f"[INFO] Trying fallback detector strategy ({alternate})...")
            try:
                boxes = _run_single_detector(image, alternate)
                if boxes:
                    print(f"[SUCCESS] Fallback strategy ({alternate}) successfully detected faces!")
                    break
            except Exception:
                continue
                
    # 4. If no face detected, return empty boxes (camera blocked or no face recorded)
    if not boxes:
        print("[INFO] No face detected or camera blocked.")
        return image, []
        
    # Clamp coordinates to image boundaries
    clamped_boxes = []
    for (x, y, bw, bh) in boxes:
        x1 = max(0, min(x, w - 1))
        y1 = max(0, min(y, h - 1))
        x2 = max(0, min(x + bw, w))
        y2 = max(0, min(y + bh, h))
        clamped_boxes.append((x1, y1, x2 - x1, y2 - y1))
        
    return image, clamped_boxes

# =====================================================================
# 6. FACE CROPPING AND TEMPORARY SAVING
# =====================================================================
def crop_and_save_faces(image, boxes, temp_dir, padding_pct=0.15):
    """Crops faces with padding, bounds clamping, and saves to temp files."""
    resolved_temp = resolve_path(temp_dir)
    if os.path.exists(resolved_temp):
        import shutil
        shutil.rmtree(resolved_temp)
    os.makedirs(resolved_temp, exist_ok=True)
    
    img_h, img_w, _ = image.shape
    crop_paths = []
    
    for idx, (x, y, w, h) in enumerate(boxes):
        pad_w = int(w * padding_pct)
        pad_h = int(h * padding_pct)
        
        x1 = max(0, x - pad_w)
        y1 = max(0, y - pad_h)
        x2 = min(img_w, x + w + pad_w)
        y2 = min(img_h, y + h + pad_h)
        
        crop = image[y1:y2, x1:x2]
        crop_path = os.path.join(resolved_temp, f"face_{idx + 1}.jpg")
        cv2.imwrite(crop_path, crop)
        crop_paths.append(crop_path)
        
    return crop_paths

# =====================================================================
# 7. IMAGE PREPROCESSING FLOW
# =====================================================================
def apply_preprocessing(crop, steps, target_size=(224, 224)):
    """Applies pipeline preprocessing steps sequentially."""
    processed = crop.copy()
    for step in steps:
        if step == 'resize':
            processed = cv2.resize(processed, target_size)
        elif step == 'lighting/contrast normalization':
            processed = apply_clahe(processed)
        elif step == 'noise reduction':
            processed = cv2.bilateralFilter(processed, d=9, sigmaColor=75, sigmaSpace=75)
        elif step == 'pixel normalization':
            processed = processed.astype(np.float32) / 255.0
    return processed

# =====================================================================
# 8. AGE DECODING AND FILENAME PARSING UTILITIES
# =====================================================================
def get_model_input_size(model, default=(224, 224)):
    """Reads Keras model input size dynamically."""
    try:
        shape = model.input_shape
        if isinstance(shape, list):
            shape = shape[0]
        if len(shape) >= 3:
            h, w = shape[1], shape[2]
            if h is not None and w is not None:
                return (w, h)
    except Exception:
        pass
    return default

def get_decoded_bin_labels(num_classes, is_cnn=True):
    """Decodes class index to appropriate categorical age labels."""
    if is_cnn:
        if num_classes == 10:
            return [f"{i}-{i+9}" for i in range(1, 100, 10)]
        elif num_classes == 3:
            return ['1-20', '21-40', '41-60']
        elif num_classes == 6:
            return [f"{i}-{i+9}" for i in range(1, 60, 10)]
    else:
        # Standard bins from MediaPipe NN references
        if num_classes == 7:
            return ["[1-10]", "[11-20]", "[21-30]", "[31-40]", "[41-50]", "[51-60]", "[71-80]"]
        elif num_classes == 9:
            return [f"[{i}-{i+9}]" for i in range(1, 90, 10)]
    return [f"Class_{i}" for i in range(num_classes)]

def parse_ground_truth_age(image_path):
    """Parses ground-truth age from filenames starting with standard UTKFace formatting."""
    base = os.path.basename(image_path)
    parts = base.split('_')
    if len(parts) >= 3 and parts[0].isdigit():
        return int(parts[0])
    return None

def map_age_to_bin(age, bin_labels):
    """Maps numerical age to matching label by parsing the bounds using regex."""
    if age is None:
        return None
    for label in bin_labels:
        # Remove bounds and brackets
        clean = label.replace('[', '').replace(']', '').replace('(', '').replace(')', '')
        if '+' in clean:
            parts = clean.split('+')
            if parts[0].strip().isdigit():
                start = int(parts[0].strip())
                if age >= start:
                    return label
        else:
            nums = re.findall(r'\d+', clean)
            if len(nums) >= 2:
                start, end = int(nums[0]), int(nums[1])
                if start <= age <= end:
                    return label
    return None

# =====================================================================
# 9. LANDMARK EXTRACTION FOR MEDIAPIPE NN
# =====================================================================
def extract_landmarks(crop_path):
    """Extracts 3D landmarks (1434 features) using modern MediaPipe task API."""
    if mp is None:
        raise ImportError("MediaPipe is not installed.")
        
    task_path = download_mediapipe_task(Paths["mediapipe_task_url"], Paths["mediapipe_task_local"])
    base_options = python.BaseOptions(model_asset_path=task_path)
    options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        output_face_blendshapes=False,
        output_facial_transformation_matrixes=False,
        num_faces=1
    )
    
    img = cv2.imread(crop_path)
    if img is None:
        raise ValueError(f"Could not read crop file: {crop_path}")
        
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    
    with vision.FaceLandmarker.create_from_options(options) as landmarker:
        res = landmarker.detect(mp_img)
        if not res.face_landmarks:
            raise ValueError(f"No landmarks detected for {crop_path}")
            
        vector = []
        for lm in res.face_landmarks[0]:
            vector.extend([lm.x, lm.y, lm.z])
        return np.array(vector, dtype=np.float32).reshape(1, -1)

# =====================================================================
# 10. MAIN PIPELINE EXECUTION
# =====================================================================
def run_pipeline():
    input_img = resolve_path(IO["input_image_path"])
    print(f"[INFO] Input image path: {input_img}")
    if not os.path.exists(input_img):
        print(f"[ERROR] Input file error: File does not exist at {input_img}")
        return
        
    # 1. Detection Stage
    print(f"\n[INFO] Running Detection Stage (Model Selection = {Model_Selection})...")
    try:
        image, boxes = detect_faces(input_img, Model_Selection)
        print(f"[SUCCESS] Face detection phase completed. Found {len(boxes)} face(s).")
    except Exception as e:
        print(f"[ERROR] Detection stage fatal error: {e}")
        return
        
    # 2. Cropping & Saving
    temp_dir = resolve_path(IO["temp_face_dir"])
    crop_paths = crop_and_save_faces(image, boxes, temp_dir)
    print(f"[INFO] Saved {len(crop_paths)} face crops into: {temp_dir}")
    
    # 3. Model & Scaler Selection
    actual_age = parse_ground_truth_age(input_img)
    y_true = []
    y_pred = []
    
    log_records = []
    
    if NeedCNN:
        bin_count = bins_Available[bin_Selected]
        models_list = Paths["convnext_models"].get(bin_count, [])
        if not models_list or ConvNextTiny_Select >= len(models_list):
            print(f"[ERROR] Model path error: ConvNeXt model not found for bin_count={bin_count} index={ConvNextTiny_Select}")
            return
            
        model_path = resolve_path(models_list[ConvNextTiny_Select])
        print(f"[INFO] Loading ConvNeXt-Tiny CNN Model ({bin_count} bins): {model_path}")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file missing at: {model_path}")
            
        model = tf.keras.models.load_model(model_path)
        
        # Read dataset metadata (labels, shape)
        scalar_path = resolve_path(Paths["convnext_scaler"])
        print(f"[INFO] Loading ConvNeXt scalar metadata: {scalar_path}")
        if os.path.exists(scalar_path):
            metadata = joblib.load(scalar_path)
            bin_labels = metadata.get('bin_labels', get_decoded_bin_labels(bin_count, is_cnn=True))
            # Clean brackets if any in metadata
            bin_labels = [b.replace('[', '').replace(']', '') for b in bin_labels]
        else:
            print("[WARNING] Metadata scalar pkl not found. Generating default ConvNeXt bins.")
            bin_labels = get_decoded_bin_labels(bin_count, is_cnn=True)
            
        input_size = get_model_input_size(model, default=(224, 224))
        
        # For each face crop
        for i, crop_p in enumerate(crop_paths):
            crop_img = cv2.imread(crop_p)
            
            if Preprocessing:
                crop_img = apply_preprocessing(crop_img, Preprocessing_Steps, target_size=input_size)
                # Ensure float32 color shape and bounds compatibility
                if crop_img.shape[:2] != input_size[::-1]:
                    crop_img = cv2.resize(crop_img, input_size)
                if 'pixel normalization' not in Preprocessing_Steps:
                    crop_img = crop_img.astype(np.float32)
            else:
                crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
                crop_img = cv2.resize(crop_img, input_size)
                crop_img = crop_img.astype(np.float32)
                
            # Expand batch dimension
            if len(crop_img.shape) == 3:
                crop_img = np.expand_dims(crop_img, axis=0)
                
            probs = model.predict(crop_img, verbose=0)[0]
            pred_idx = np.argmax(probs)
            pred_label = bin_labels[pred_idx] if pred_idx < len(bin_labels) else f"Class_{pred_idx}"
            confidence = float(probs[pred_idx])
            
            true_bin = map_age_to_bin(actual_age, bin_labels)
            ground_truth_str = f"{actual_age} (Bin: {true_bin})" if actual_age is not None else "N/A"
            
            print(f"[LOG] face_{i+1} - Actual Age: {ground_truth_str} - Predicted Bin: {pred_label} ({confidence * 100:.2f}%)")
            
            log_records.append({
                "face_index": i + 1,
                "crop_path": crop_p,
                "actual_age": actual_age,
                "actual_bin": true_bin,
                "predicted_bin": pred_label,
                "confidence": confidence
            })
            
            if true_bin is not None:
                y_true.append(true_bin)
                y_pred.append(pred_label)
                
    else:
        # MediaPipe Landmark NN Path
        models_list = Paths["mediapipe_nn_models"]
        if not models_list or MediaPipe_LandMark_NN >= len(models_list):
            print(f"[ERROR] Model path error: MediaPipe NN model not found at index={MediaPipe_LandMark_NN}")
            return
            
        model_path = resolve_path(models_list[MediaPipe_LandMark_NN])
        print(f"[INFO] Loading MediaPipe Landmark NN Model: {model_path}")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file missing at: {model_path}")
            
        model = tf.keras.models.load_model(model_path)
        
        # Load scaler
        scaler_path = resolve_path(Paths["mediapipe_scaler"])
        print(f"[INFO] Loading MediaPipe scalar: {scaler_path}")
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(f"MediaPipe Scaler file missing at: {scaler_path}")
        scaler = joblib.load(scaler_path)
        
        num_classes = model.output_shape[1]
        bin_labels = get_decoded_bin_labels(num_classes, is_cnn=False)
        
        # For each face crop
        for i, crop_p in enumerate(crop_paths):
            try:
                landmarks = extract_landmarks(crop_p)
            except Exception as e:
                print(f"[WARNING] Could not extract landmarks for face_{i+1}: {e}. Skipping prediction.")
                continue
                
            expected_dim = model.input_shape[1]
            if landmarks.shape[1] > expected_dim:
                landmarks = landmarks[:, :expected_dim]
                
            if scaler is not None:
                landmarks = scaler.transform(landmarks).astype(np.float32)
                
            probs = model.predict(landmarks, verbose=0)[0]
            pred_idx = np.argmax(probs)
            pred_label = bin_labels[pred_idx] if pred_idx < len(bin_labels) else f"Class_{pred_idx}"
            confidence = float(probs[pred_idx])
            
            true_bin = map_age_to_bin(actual_age, bin_labels)
            ground_truth_str = f"{actual_age} (Bin: {true_bin})" if actual_age is not None else "N/A"
            
            print(f"[LOG] face_{i+1} - Actual Age: {ground_truth_str} - Predicted Bin: {pred_label} ({confidence * 100:.2f}%)")
            
            log_records.append({
                "face_index": i + 1,
                "crop_path": crop_p,
                "actual_age": actual_age,
                "actual_bin": true_bin,
                "predicted_bin": pred_label,
                "confidence": confidence
            })
            
            if true_bin is not None:
                y_true.append(true_bin)
                y_pred.append(pred_label)
                
    # 4. Save results to log
    log_dir = resolve_path(IO["results_log"])
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, f"age_prediction_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    with open(log_file_path, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "config": {
                "Model_Selection": Model_Selection,
                "Preprocessing": Preprocessing,
                "NeedCNN": NeedCNN,
                "bin_Selected": bin_Selected,
                "ConvNextTiny_Select": ConvNextTiny_Select,
                "MediaPipe_LandMark_NN": MediaPipe_LandMark_NN
            },
            "predictions": log_records
        }, f, indent=4)
    print(f"\n[INFO] Run results logged to: {log_file_path}")
    
    # 5. Compute Metrics if ground truth exists
    if y_true and y_pred:
        acc = accuracy_score(y_true, y_pred)
        prec, rec, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
        
        print("\n" + "=" * 50)
        print("[METRICS] AGGREGATE EVALUATION METRICS")
        print("=" * 50)
        print(f"Accuracy  : {acc * 100:.2f}%")
        print(f"Precision : {prec:.4f}")
        print(f"Recall    : {rec:.4f}")
        print(f"F1 Score  : {f1:.4f}")
        print("=" * 50 + "\n")
    elif actual_age is not None:
        print("\n[WARNING] No predictions were aligned with ground-truth bins. Bins might be mismatched or empty.")
    else:
        print("\n[INFO] Ground-truth labels are not available. Evaluation metrics skipped.")

def predict_face_age(image_path, model_selection=None, need_cnn=None, bin_selected=None, convnext_select=None, mediapipe_nn_select=None):
    """
    Inference helper for web API. Returns a dict containing face detection, cropping paths,
    predicted classes, confidence scores, and mapped VoiceVision age category ("Below 18" or "18 or Above").
    """
    if model_selection is None:
        model_selection = Model_Selection
    if need_cnn is None:
        need_cnn = NeedCNN
    if bin_selected is None:
        bin_selected = bin_Selected
    if convnext_select is None:
        convnext_select = ConvNextTiny_Select
    if mediapipe_nn_select is None:
        mediapipe_nn_select = MediaPipe_LandMark_NN

    resolved_img = resolve_path(image_path)
    if not os.path.exists(resolved_img):
        return {"success": False, "error": f"Image path does not exist: {resolved_img}"}

    # 1. Detection
    image, boxes = detect_faces(resolved_img, model_selection)
    if not boxes:
        return {
            "success": False,
            "face_detected": False,
            "error": "Face is not recorder",
            "message": "Face is not recorder"
        }

    # 2. Crop
    temp_dir = resolve_path(IO["temp_face_dir"])
    crop_paths = crop_and_save_faces(image, boxes, temp_dir)
    if not crop_paths:
        return {"success": False, "error": "Failed to crop face regions."}

    predictions = []

    # 3. Predict per crop
    if need_cnn:
        bin_count = bins_Available[bin_selected]
        models_list = Paths["convnext_models"].get(bin_count, [])
        if not models_list or convnext_select >= len(models_list):
            return {"success": False, "error": f"ConvNeXt model index {convnext_select} not found for bin_count {bin_count}."}
        model_path = resolve_path(models_list[convnext_select])
        model = tf.keras.models.load_model(model_path)

        scalar_path = resolve_path(Paths["convnext_scaler"])
        if os.path.exists(scalar_path):
            metadata = joblib.load(scalar_path)
            bin_labels = metadata.get('bin_labels', get_decoded_bin_labels(bin_count, is_cnn=True))
            bin_labels = [b.replace('[', '').replace(']', '') for b in bin_labels]
        else:
            bin_labels = get_decoded_bin_labels(bin_count, is_cnn=True)

        input_size = get_model_input_size(model, default=(224, 224))

        for idx, crop_p in enumerate(crop_paths):
            crop_img = cv2.imread(crop_p)
            crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
            crop_img = cv2.resize(crop_img, input_size)
            crop_img = crop_img.astype(np.float32)
            if len(crop_img.shape) == 3:
                crop_img = np.expand_dims(crop_img, axis=0)

            probs = model.predict(crop_img, verbose=0)[0]
            pred_idx = np.argmax(probs)
            pred_label = bin_labels[pred_idx] if pred_idx < len(bin_labels) else f"Class_{pred_idx}"
            confidence = float(probs[pred_idx])

            # Map predicted bin to VoiceVision category
            clean_label = pred_label.replace('[', '').replace(']', '')
            is_child = False
            nums = re.findall(r'\d+', clean_label)
            if nums:
                max_age_in_bin = max(map(int, nums))
                if max_age_in_bin <= 20:
                    is_child = True
            mapped_class = "Below 18" if is_child else "18 or Above"

            predictions.append({
                "face_index": idx + 1,
                "crop_relative_path": os.path.relpath(crop_p, os.path.dirname(os.path.abspath(__file__))).replace("\\", "/"),
                "predicted_bin": pred_label,
                "confidence": confidence,
                "mapped_class": mapped_class
            })
    else:
        models_list = Paths["mediapipe_nn_models"]
        if not models_list or mediapipe_nn_select >= len(models_list):
            return {"success": False, "error": f"MediaPipe NN model index {mediapipe_nn_select} not found."}
        model_path = resolve_path(models_list[mediapipe_nn_select])
        model = tf.keras.models.load_model(model_path)

        scaler_path = resolve_path(Paths["mediapipe_scaler"])
        scaler = joblib.load(scaler_path)

        num_classes = model.output_shape[1]
        bin_labels = get_decoded_bin_labels(num_classes, is_cnn=False)

        for idx, crop_p in enumerate(crop_paths):
            try:
                landmarks = extract_landmarks(crop_p)
            except Exception as e:
                continue

            expected_dim = model.input_shape[1]
            if landmarks.shape[1] > expected_dim:
                landmarks = landmarks[:, :expected_dim]

            if scaler is not None:
                landmarks = scaler.transform(landmarks).astype(np.float32)

            probs = model.predict(landmarks, verbose=0)[0]
            pred_idx = np.argmax(probs)
            pred_label = bin_labels[pred_idx] if pred_idx < len(bin_labels) else f"Class_{pred_idx}"
            confidence = float(probs[pred_idx])

            clean_label = pred_label.replace('[', '').replace(']', '')
            is_child = False
            nums = re.findall(r'\d+', clean_label)
            if nums:
                max_age_in_bin = max(map(int, nums))
                if max_age_in_bin <= 20:
                    is_child = True
            mapped_class = "Below 18" if is_child else "18 or Above"

            predictions.append({
                "face_index": idx + 1,
                "crop_relative_path": os.path.relpath(crop_p, os.path.dirname(os.path.abspath(__file__))).replace("\\", "/"),
                "predicted_bin": pred_label,
                "confidence": confidence,
                "mapped_class": mapped_class
            })

    if not predictions:
        return {"success": False, "error": "Landmark extraction or predictions failed on all faces."}

    overall_class = "18 or Above"
    if any(p["mapped_class"] == "Below 18" for p in predictions):
        overall_class = "Below 18"

    return {
        "success": True,
        "overall_class": overall_class,
        "predictions": predictions
    }

if __name__ == "__main__":
    run_pipeline()
