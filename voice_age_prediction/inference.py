import os
import argparse
import numpy as np
import tensorflow as tf
from tensorflow import keras

import config
import preprocessing
import features

def predict_age_group(audio_path, model_path=None, threshold=None):
    """
    Predicts the age group (Below 18 or 18 or Above) from a voice recording.
    
    Args:
        audio_path (str): Path to the input wav/mp3 file.
        model_path (str): Path to the trained .keras model.
        threshold (float): Classification threshold.
        
    Returns:
        dict: Predictions including class, probability, and confidence.
    """
    # 1. Set defaults
    if model_path is None:
        model_path = os.path.join(config.MODEL_DIR, "best_model.keras")
    if threshold is None:
        threshold = config.DEFAULT_THRESHOLD
        
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found at {audio_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Trained model not found at {model_path}. Please train a model first.")
        
    # 2. Preprocess audio
    waveform = preprocessing.preprocess_audio(audio_path)
    
    # 3. Extract features
    if getattr(config, "USE_ENGINEERED_FEATURES", False):
        feat = features.extract_engineered_features(waveform)
        # Load scaling parameters
        scalers_path = os.path.join(config.MODEL_DIR, "scalers.npz")
        if os.path.exists(scalers_path):
            scalers = np.load(scalers_path)
            mean = scalers["mean"]
            std = scalers["std"]
            feat = (feat - mean) / std
        else:
            print("Warning: scalers.npz not found for engineered features!")
    elif config.USE_MFCC:
        feat = features.extract_mfcc(waveform)
    else:
        feat = features.extract_log_mel_spectrogram(waveform)
        
    # 4. Add batch dimension
    feat_batch = np.expand_dims(feat, axis=0)
    
    # 5. Load model and predict
    model = keras.models.load_model(model_path)
    prob = float(model.predict(feat_batch, verbose=0)[0][0])
    
    # 6. Apply threshold and calculate confidence
    if prob >= threshold:
        predicted_class = "18 or Above"
        confidence = prob
    else:
        predicted_class = "Below 18"
        confidence = 1.0 - prob
        
    return {
        "predicted_class": predicted_class,
        "probability": prob,
        "confidence": confidence,
        "threshold_used": threshold
    }

def main():
    parser = argparse.ArgumentParser(description="Inference tool for voice-based age classification.")
    parser.add_argument("--audio", type=str, required=True, help="Path to input audio file (.wav or .mp3)")
    parser.add_argument("--model", type=str, default=None, help="Path to trained .keras model file")
    parser.add_argument("--threshold", type=float, default=None, help="Classification probability threshold")
    args = parser.parse_args()
    
    try:
        res = predict_age_group(args.audio, args.model, args.threshold)
        print("\n=========================================")
        print("         Age Group Classification        ")
        print("=========================================")
        print(f"Predicted Age Group: {res['predicted_class']}")
        print(f"Probability:         {res['probability']:.4f}")
        print(f"Confidence:          {res['confidence'] * 100:.1f}%")
        print(f"Threshold:           {res['threshold_used']:.2f}")
        print("=========================================\n")
    except Exception as e:
        print(f"Error during inference: {e}")

if __name__ == "__main__":
    main()
