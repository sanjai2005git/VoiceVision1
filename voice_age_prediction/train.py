import os
import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.utils.class_weight import compute_class_weight

import config
from dataset import load_and_preprocess_metadata, split_by_speaker, VoiceDatasetGenerator
from model import build_cnn_lstm_model

def main():
    print("=========================================")
    print("   Starting Voice Age Classifier Training")
    print("=========================================")
    
    # 1. Load metadata
    df = load_and_preprocess_metadata(config.DATA_DIR)
    
    # 2. Count class distribution and calculate class weights
    labels = df["label"].values
    unique_classes = np.unique(labels)
    class_counts = np.bincount(labels)
    
    print("\n--- Class Distribution ---")
    for cls in unique_classes:
        class_name = "Below 18 (Class 0)" if cls == 0 else "18 or Above (Class 1)"
        count = class_counts[cls]
        pct = (count / len(df)) * 100
        print(f"  {class_name}: {count} samples ({pct:.2f}%)")
    print("--------------------------\n")
    
    # Calculate balanced class weights
    weights = compute_class_weight(
        class_weight="balanced",
        classes=unique_classes,
        y=labels
    )
    class_weights = {int(cls): float(w) for cls, w in zip(unique_classes, weights)}
    print(f"Calculated class weights: {class_weights}\n")
    
    # 3. Split dataset by speaker (speaker-independent splitting)
    train_df, val_df, test_df = split_by_speaker(df)
    
    # Apply optional subset scaling for quick testing
    if config.SUBSET_FRACTION is not None:
        print(f"[Warning] SUBSET_FRACTION is set to {config.SUBSET_FRACTION}. Reducing datasets.")
        # Filter train/val/test dataframes keeping a representative subset fraction
        train_df = train_df.sample(frac=config.SUBSET_FRACTION, random_state=42).reset_index(drop=True)
        val_df = val_df.sample(frac=config.SUBSET_FRACTION, random_state=42).reset_index(drop=True)
        test_df = test_df.sample(frac=config.SUBSET_FRACTION, random_state=42).reset_index(drop=True)
        print(f"New sizes -> Train: {len(train_df)} | Val: {len(val_df)} | Test: {len(test_df)}\n")
        
    # Save the splits to CSV for evaluation module usage
    train_df.to_csv(os.path.join(config.DATA_DIR, "train_split.csv"), index=False)
    val_df.to_csv(os.path.join(config.DATA_DIR, "val_split.csv"), index=False)
    test_df.to_csv(os.path.join(config.DATA_DIR, "test_split.csv"), index=False)
    
    # Check if we have enough samples to train
    if len(train_df) < config.BATCH_SIZE:
        print(f"Error: Train split size ({len(train_df)}) is less than BATCH_SIZE ({config.BATCH_SIZE}).")
        print("Please increase dataset size or disable/increase SUBSET_FRACTION in config.py.")
        return
        
    # 4. Instantiate data generators
    print("Initializing Voice Dataset Generators...")
    train_gen = VoiceDatasetGenerator(
        df=train_df,
        batch_size=config.BATCH_SIZE,
        augment=True,
        use_mfcc=config.USE_MFCC,
        shuffle=True
    )
    val_gen = VoiceDatasetGenerator(
        df=val_df,
        batch_size=config.BATCH_SIZE,
        augment=False,
        use_mfcc=config.USE_MFCC,
        shuffle=False
    )
    
    input_shape = train_gen.input_shape
    print(f"Input Feature Shape: {input_shape}")
    print(f"Using MFCC representation: {config.USE_MFCC}\n")
    
    # 5. Build and Compile model
    print("Building CNN + BiLSTM model...")
    model = build_cnn_lstm_model(
        input_shape=input_shape,
        cnn_filters=config.CNN_FILTERS,
        lstm_units=config.LSTM_UNITS,
        dropout_rate=config.DROPOUT,
        learning_rate=config.LEARNING_RATE
    )
    model.summary()
    
    # 6. Callbacks
    best_model_path = os.path.join(config.MODEL_DIR, "best_model.keras")
    
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=6,
            restore_best_weights=True,
            verbose=1
        ),
        keras.callbacks.ModelCheckpoint(
            filepath=best_model_path,
            monitor="val_loss",
            save_best_only=True,
            verbose=1
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            min_lr=1e-6,
            verbose=1
        )
    ]
    
    # 7. Model training
    print(f"\nStarting training for {config.EPOCHS} epochs...")
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=config.EPOCHS,
        class_weight=class_weights,
        callbacks=callbacks
    )
    
    # Save training history to json
    history_dict = history.history
    history_path = os.path.join(config.MODEL_DIR, "history.json")
    with open(history_path, "w") as f:
        json.dump(history_dict, f, indent=4)
        
    # Save feature scalers
    if getattr(config, "USE_ENGINEERED_FEATURES", False):
        scalers_path = os.path.join(config.MODEL_DIR, "scalers.npz")
        np.savez(scalers_path, mean=train_gen.mean, std=train_gen.std)
        print(f"Saved feature scalers to: {scalers_path}")
        
    print(f"\nTraining completed! Best model saved to: {best_model_path}")
    print(f"Training history saved to: {history_path}")

if __name__ == "__main__":
    main()
