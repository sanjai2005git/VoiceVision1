import os
import joblib
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
import mediapipe as mp
import argparse

# Constants and paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Face Recognition Models and scaler are inside the sibling directory
FACE_MODELS_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "Age_Recognition-20260828T133809Z-1-001", "Age_Recognition", "Models"))

MODEL_PATH = os.path.join(FACE_MODELS_DIR, "indface_20260722_094646.keras")
SCALER_PATH = os.path.join(FACE_MODELS_DIR, "scaler.pkl")

# Human-readable labels for the 7 output categories
AGE_LABELS = {
    0: "0-12 (Child)",
    1: "13-20 (Teenager)",
    2: "21-30 (Young Adult)",
    3: "31-40 (Adult)",
    4: "41-50 (Middle-aged)",
    5: "51-60 (Late Middle-aged)",
    6: "61+ (Senior)"
}

class FaceAgePredictor:
    def __init__(self, model_path=MODEL_PATH, scaler_path=SCALER_PATH):
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = None
        self.scaler = None
        
        # Load scaler
        if os.path.exists(self.scaler_path):
            self.scaler = joblib.load(self.scaler_path)
        else:
            raise FileNotFoundError(f"Scaler not found at {self.scaler_path}")
            
        # Load keras model
        if os.path.exists(self.model_path):
            self.model = keras.models.load_model(self.model_path)
        else:
            raise FileNotFoundError(f"Keras model not found at {self.model_path}")
            
    def predict_image(self, image_path, output_annotated_path=None):
        """
        Extract landmarks, draw them on the image, run inference, and return the predicted age group.
        
        Args:
            image_path (str): Path to input image.
            output_annotated_path (str): Optional path to save the landmark-annotated image.
            
        Returns:
            dict: Predictions including class index, label, confidence, and success status.
        """
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from path: {image_path}")
            
        # Initialize mediapipe face mesh
        mp_face_mesh = mp.solutions.face_mesh
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles
        
        with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        ) as face_mesh:
            
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_image)
            
            if not results.multi_face_landmarks:
                return {
                    "success": False,
                    "error": "No face detected in the image."
                }
                
            # Get the first face
            face_landmarks = results.multi_face_landmarks[0]
            
            # Extract coordinates for all 478 landmarks (1434 features)
            landmarks = []
            for landmark in face_landmarks.landmark:
                landmarks.extend([landmark.x, landmark.y, landmark.z])
                
            if len(landmarks) != 1434:
                return {
                    "success": False,
                    "error": f"Incorrect number of landmarks detected. Expected 1434, got {len(landmarks)}."
                }
                
            # Scale landmarks using StandardScaler
            features_scaled = self.scaler.transform([landmarks])
            
            # Predict using model
            preds = self.model.predict(features_scaled, verbose=0)[0]
            class_idx = int(np.argmax(preds))
            confidence = float(preds[class_idx])
            predicted_label = AGE_LABELS.get(class_idx, "Unknown")
            
            # Save annotated image if requested
            if output_annotated_path:
                annotated_image = image.copy()
                
                # Draw tesselation
                mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                )
                # Draw contours
                mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
                )
                # Draw irises
                mp_drawing.draw_landmarks(
                    image=annotated_image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style()
                )
                
                # Ensure the folder exists
                os.makedirs(os.path.dirname(output_annotated_path), exist_ok=True)
                cv2.imwrite(output_annotated_path, annotated_image)
                
            probabilities_dict = {AGE_LABELS[i]: float(p) for i, p in enumerate(preds)}
            
            # Return prediction results
            return {
                "success": True,
                "class_index": class_idx,
                "predicted_class": predicted_label,
                "confidence": confidence,
                "probabilities": probabilities_dict
            }

def main():
    parser = argparse.ArgumentParser(description="Inference tool for face-based age classification.")
    parser.add_argument("--image", type=str, required=True, help="Path to input image file")
    parser.add_argument("--output", type=str, default=None, help="Path to save annotated output image")
    args = parser.parse_args()
    
    try:
        predictor = FaceAgePredictor()
        res = predictor.predict_image(args.image, args.output)
        if res["success"]:
            print("\n=========================================")
            print("         Face Age Classification        ")
            print("=========================================")
            print(f"Predicted Age Group: {res['predicted_class']}")
            print(f"Confidence:          {res['confidence'] * 100:.1f}%")
            print("=========================================")
            print("Probabilities:")
            for label, prob in res["probabilities"].items():
                print(f"  {label:<25}: {prob * 100:.2f}%")
            print("=========================================\n")
        else:
            print(f"Error: {res['error']}")
    except Exception as e:
        print(f"Error during face inference: {e}")

if __name__ == "__main__":
    main()
