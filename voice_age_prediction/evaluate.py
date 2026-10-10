import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix
)
from tqdm import tqdm

import config
import preprocessing
import features

def predict_dataset(df, model, desc="Predicting"):
    """
    Predicts age probabilities for a given dataframe of voice paths.
    """
    probs = []
    labels = []
    paths = []
    
    # Load scaling parameters if using engineered features
    mean = None
    std = None
    if getattr(config, "USE_ENGINEERED_FEATURES", False):
        scalers_path = os.path.join(config.MODEL_DIR, "scalers.npz")
        if os.path.exists(scalers_path):
            scalers = np.load(scalers_path)
            mean = scalers["mean"]
            std = scalers["std"]
        else:
            print("Warning: scalers.npz not found for engineered features!")

    for idx, row in tqdm(df.iterrows(), total=len(df), desc=desc):
        path = row["full_audio_path"]
        lbl = row["label"]
        
        try:
            # Load and preprocess
            waveform = preprocessing.preprocess_audio(path)
            
            # Extract features
            if getattr(config, "USE_ENGINEERED_FEATURES", False):
                feat = features.extract_engineered_features(waveform)
                if mean is not None:
                    feat = (feat - mean) / std
            elif config.USE_MFCC:
                feat = features.extract_mfcc(waveform)
            else:
                feat = features.extract_log_mel_spectrogram(waveform)
                
            # Add batch dimension
            feat_batch = np.expand_dims(feat, axis=0)
            
            # Run inference
            prob = model.predict(feat_batch, verbose=0)[0][0]
            
            probs.append(prob)
            labels.append(lbl)
            paths.append(path)
        except Exception as e:
            print(f"Error predicting for {path}: {e}")
            
    return np.array(probs), np.array(labels), paths

def calculate_metrics(labels, probs, threshold):
    """
    Computes all standard binary classification metrics.
    """
    preds = (probs >= threshold).astype(int)
    
    acc = accuracy_score(labels, preds)
    prec = precision_score(labels, preds, zero_division=0)
    rec = recall_score(labels, preds, zero_division=0)
    f1 = f1_score(labels, preds, zero_division=0)
    
    try:
        auc = roc_auc_score(labels, probs)
    except ValueError:
        auc = 0.5  # In case of single class in batch
        
    cm = confusion_matrix(labels, preds)
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
    else:
        # Handle cases where one class is completely missing
        tn = cm[0, 0] if 0 in labels else 0
        tp = cm[0, 0] if 1 in labels else 0
        fp = fn = 0
        
    sensitivity = tp / (tp + fn + 1e-8)
    specificity = tn / (tn + fp + 1e-8)
    
    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "auc": auc,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "tp": tp,
        "sensitivity": sensitivity,
        "specificity": specificity
    }

def plot_training_curves(history_path, save_dir):
    """
    Plots training vs validation accuracy and loss curves from training history JSON.
    """
    if not os.path.exists(history_path):
        print(f"History file not found at {history_path}. Skipping training curves.")
        return
        
    with open(history_path, "r") as f:
        history = json.load(f)
        
    epochs = range(1, len(history["accuracy"]) + 1)
    
    # 1. Accuracy Curve
    plt.figure(figsize=(8, 5))
    plt.plot(epochs, history["accuracy"], "b-o", label="Training Accuracy")
    plt.plot(epochs, history["val_accuracy"], "r-s", label="Validation Accuracy")
    plt.title("Training vs Validation Accuracy")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "accuracy_curves.png"), dpi=300)
    plt.close()
    
    # 2. Loss Curve
    plt.figure(figsize=(8, 5))
    plt.plot(epochs, history["loss"], "b-o", label="Training Loss")
    plt.plot(epochs, history["val_loss"], "r-s", label="Validation Loss")
    plt.title("Training vs Validation Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "loss_curves.png"), dpi=300)
    plt.close()
    print("Saved training vs validation accuracy & loss curves.")

def plot_confusion_matrix(tn, fp, fn, tp, threshold, save_dir):
    """
    Plots a stylized confusion matrix.
    """
    cm = np.array([[tn, fp], [fn, tp]])
    classes = ["Below 18 (Class 0)", "18 or Above (Class 1)"]
    
    plt.figure(figsize=(6, 5))
    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title(f"Confusion Matrix (Thresh = {threshold:.2f})")
    plt.colorbar()
    
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=15)
    plt.yticks(tick_marks, classes)
    
    # Label cell counts
    thresh = cm.max() / 2.0
    for i in range(2):
        for j in range(2):
            plt.text(
                j, i, format(cm[i, j], "d"),
                horizontalalignment="center",
                color="white" if cm[i, j] > thresh else "black",
                fontsize=14
            )
            
    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "confusion_matrix.png"), dpi=300)
    plt.close()
    print("Saved confusion matrix heatmap.")

def plot_roc_curve(labels, probs, auc_score, save_dir):
    """
    Plots the ROC Curve.
    """
    fpr, tpr, _ = roc_curve(labels, probs)
    
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, color="darkorange", lw=2, label=f"ROC Curve (AUC = {auc_score:.4f})")
    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate (1 - Specificity)")
    plt.ylabel("True Positive Rate (Sensitivity)")
    plt.title("Receiver Operating Characteristic (ROC)")
    plt.legend(loc="lower right")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "roc_curve.png"), dpi=300)
    plt.close()
    print("Saved ROC curve plot.")

def plot_class_distribution(train_df, val_df, test_df, save_dir):
    """
    Plots the distribution of classes across all data splits.
    """
    categories = ["Train", "Val", "Test"]
    below_18_counts = [
        sum(train_df["label"] == 0),
        sum(val_df["label"] == 0),
        sum(test_df["label"] == 0)
    ]
    above_18_counts = [
        sum(train_df["label"] == 1),
        sum(val_df["label"] == 1),
        sum(test_df["label"] == 1)
    ]
    
    x = np.arange(len(categories))
    width = 0.35
    
    plt.figure(figsize=(7, 5))
    plt.bar(x - width/2, below_18_counts, width, label="Below 18 (Class 0)", color="#3498db")
    plt.bar(x + width/2, above_18_counts, width, label="18 or Above (Class 1)", color="#e74c3c")
    
    plt.ylabel("Sample Count")
    plt.title("Age-Group Class Distribution across splits")
    plt.xticks(x, categories)
    plt.legend()
    plt.grid(axis='y', linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "class_distribution.png"), dpi=300)
    plt.close()
    print("Saved class distribution plot.")

def main():
    print("=========================================")
    print("      Evaluating Voice Age Classifier    ")
    print("=========================================")
    
    # 1. Load trained model
    model_path = os.path.join(config.MODEL_DIR, "best_model.keras")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Trained model not found at {model_path}. Please run train.py first.")
        
    print(f"Loading trained Keras model from {model_path}...")
    model = keras.models.load_model(model_path)
    
    # 2. Load splits
    train_split_path = os.path.join(config.DATA_DIR, "train_split.csv")
    val_split_path = os.path.join(config.DATA_DIR, "val_split.csv")
    test_split_path = os.path.join(config.DATA_DIR, "test_split.csv")
    
    if not (os.path.exists(val_split_path) and os.path.exists(test_split_path)):
        raise FileNotFoundError("Split CSVs not found in data directory. Please run train.py first.")
        
    train_df = pd.read_csv(train_split_path)
    val_df = pd.read_csv(val_split_path)
    test_df = pd.read_csv(test_split_path)
    
    # 3. Generate predictions (probabilities)
    print("\nPredicting on Validation Set...")
    val_probs, val_labels, _ = predict_dataset(val_df, model, "Val predictions")
    
    print("\nPredicting on Test Set...")
    test_probs, test_labels, test_paths = predict_dataset(test_df, model, "Test predictions")
    
    # 4. Threshold analysis on Validation Set
    print("\n--- Threshold Analysis on Validation Set ---")
    thresholds = [0.30, 0.40, 0.50, 0.60, 0.70]
    best_thresh = 0.5
    best_val_f1 = -1
    
    for th in thresholds:
        metrics = calculate_metrics(val_labels, val_probs, th)
        print(f"Threshold: {th:.2f} | Acc: {metrics['accuracy']:.4f} | Prec: {metrics['precision']:.4f} | Rec: {metrics['recall']:.4f} | F1: {metrics['f1']:.4f}")
        
        if metrics['f1'] > best_val_f1:
            best_val_f1 = metrics['f1']
            best_thresh = th
            
    print(f"--> Selected Optimal Threshold: {best_thresh:.2f} (Maximized Validation F1-score: {best_val_f1:.4f})\n")
    
    # 5. Evaluate on Test Set
    print("--- Evaluating on Unseen Speakers (Test Set) ---")
    print(f"**Speaker-Independent Evaluation**: Note that the {len(test_df['client_id'].unique())} test speakers were NEVER used during training or validation.\n")
    
    # A. Default 0.5 Threshold
    metrics_05 = calculate_metrics(test_labels, test_probs, 0.5)
    print("=== Test Set Results with DEFAULT Threshold (0.50) ===")
    print(f"Accuracy:    {metrics_05['accuracy']:.4f}")
    print(f"Precision:   {metrics_05['precision']:.4f}")
    print(f"Recall:      {metrics_05['recall']:.4f}")
    print(f"F1-Score:    {metrics_05['f1']:.4f}")
    print(f"ROC-AUC:     {metrics_05['auc']:.4f}")
    print(f"Sensitivity: {metrics_05['sensitivity']:.4f}")
    print(f"Specificity: {metrics_05['specificity']:.4f}")
    print(f"Confusion Matrix: TP={metrics_05['tp']}, TN={metrics_05['tn']}, FP={metrics_05['fp']}, FN={metrics_05['fn']}\n")
    
    # B. Optimized Threshold
    metrics_opt = calculate_metrics(test_labels, test_probs, best_thresh)
    print(f"=== Test Set Results with OPTIMIZED Threshold ({best_thresh:.2f}) ===")
    print(f"Accuracy:    {metrics_opt['accuracy']:.4f}")
    print(f"Precision:   {metrics_opt['precision']:.4f}")
    print(f"Recall:      {metrics_opt['recall']:.4f}")
    print(f"F1-Score:    {metrics_opt['f1']:.4f}")
    print(f"ROC-AUC:     {metrics_opt['auc']:.4f}")
    print(f"Sensitivity: {metrics_opt['sensitivity']:.4f}")
    print(f"Specificity: {metrics_opt['specificity']:.4f}")
    print(f"Confusion Matrix: TP={metrics_opt['tp']}, TN={metrics_opt['tn']}, FP={metrics_opt['fp']}, FN={metrics_opt['fn']}\n")
    
    # 6. Generate and save all plots
    print("Generating figures...")
    plot_training_curves(os.path.join(config.MODEL_DIR, "history.json"), config.MODEL_DIR)
    plot_confusion_matrix(metrics_opt['tn'], metrics_opt['fp'], metrics_opt['fn'], metrics_opt['tp'], best_thresh, config.MODEL_DIR)
    plot_roc_curve(test_labels, test_probs, metrics_opt['auc'], config.MODEL_DIR)
    plot_class_distribution(train_df, val_df, test_df, config.MODEL_DIR)
    
    # 7. Error Analysis
    print("\n--- Error Analysis ---")
    test_preds = (test_probs >= best_thresh).astype(int)
    
    false_positives = []
    false_negatives = []
    
    for i in range(len(test_labels)):
        actual = test_labels[i]
        pred = test_preds[i]
        prob = test_probs[i]
        path = test_paths[i]
        
        if actual == 0 and pred == 1:
            false_positives.append((path, prob))
        elif actual == 1 and pred == 0:
            false_negatives.append((path, prob))
            
    print(f"\n[False Positives (Actual: Below 18, Predicted: 18+)] - Found {len(false_positives)} examples:")
    for fp_path, fp_prob in false_positives[:5]: # Print up to 5 examples
        print(f"  File: {os.path.basename(fp_path)} (Prob: {fp_prob:.4f})")
        
    print(f"\n[False Negatives (Actual: 18+, Predicted: Below 18)] - Found {len(false_negatives)} examples:")
    for fn_path, fn_prob in false_negatives[:5]: # Print up to 5 examples
        print(f"  File: {os.path.basename(fn_path)} (Prob: {fn_prob:.4f})")
        
    # Discuss potential reasons
    print("\n=== Research Discussion: Causes of Error ===")
    print("Voice-based age prediction faces several acoustic challenges:")
    print("1. Voice Maturity: Voice properties (fundamental frequency, formant frequencies) of late adolescents (16-17)")
    print("   often overlap significantly with young adults (18-22). Biological voice maturation does not align strictly")
    print("   with the legal adult threshold of 18 years.")
    print("2. Recording Quality & Acoustics: Background noise, low-quality microphones, clipping, and room reverberation")
    print("   distort the high-frequency harmonics which are crucial for resolving vocal tract length details.")
    print("3. Accent & Speaking Style: Speech patterns, prosody, and speed can influence temporal modeling layers (LSTMs).")
    print("   A highly expressive child voice might have properties resembling a high-pitched adult voice, and vice-versa.")
    print("4. Label Reliability: Self-reported metadata in crowdsourced datasets like Common Voice can contain errors")
    print("   or missing data, resulting in noisy training/evaluation labels.")
    print("============================================\n")

if __name__ == "__main__":
    main()
