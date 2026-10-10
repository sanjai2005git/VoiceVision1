import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras

import config
import preprocessing
import features
import dataset
import model
import train

def test_preprocessing():
    print("Testing preprocessing...")
    # Create a synthetic wave array
    sr = config.SAMPLING_RATE
    duration = config.AUDIO_DURATION
    target_samples = sr * duration
    
    # 3 seconds of sound, should be padded to 5 seconds (80000 samples)
    t = np.linspace(0, 3, int(sr * 3), endpoint=False)
    synthetic_wave = 0.5 * np.sin(2 * np.pi * 440 * t)
    
    # Save dummy file
    temp_wav_path = "temp_test_wave.wav"
    import soundfile as sf
    sf.write(temp_wav_path, synthetic_wave, sr)
    
    try:
        processed = preprocessing.preprocess_audio(temp_wav_path, sr=sr, duration=duration)
        assert len(processed) == target_samples, f"Expected {target_samples} samples, got {len(processed)}"
        assert np.max(np.abs(processed)) <= 1.0, "Audio should be peak-normalized"
        print("  [PASSED] Preprocessing unit test.")
    finally:
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)

def test_feature_extraction():
    print("Testing feature extraction...")
    dummy_wave = np.random.normal(size=(config.SAMPLING_RATE * config.AUDIO_DURATION))
    
    mel_feat = features.extract_log_mel_spectrogram(dummy_wave)
    # Target shape: (TimeSteps, MelBins, 1)
    # TimeSteps = ceil(80000 / hop_length) -> ceil(80000 / 160) = 500 or 501 depending on padding.
    # librosa.feature.melspectrogram defaults will yield 501 frames
    assert len(mel_feat.shape) == 3, f"Expected 3D tensor, got shape {mel_feat.shape}"
    assert mel_feat.shape[1] == config.MEL_BINS, f"Expected {config.MEL_BINS} mel bins, got {mel_feat.shape[1]}"
    assert mel_feat.shape[2] == 1, "Expected single channel"
    print(f"  [PASSED] Feature extraction unit test. Mel Spectrogram Shape: {mel_feat.shape}")
    
    mfcc_feat = features.extract_mfcc(dummy_wave)
    assert mfcc_feat.shape[1] == 20, f"Expected 20 MFCC bands, got {mfcc_feat.shape[1]}"
    assert mfcc_feat.shape[2] == 1
    print(f"  [PASSED] Feature extraction unit test. MFCC Shape: {mfcc_feat.shape}")

def test_data_leakage():
    print("Testing data leakage...")
    # Load metadata (this will generate mock dataset if none exists)
    df = dataset.load_and_preprocess_metadata(config.DATA_DIR)
    
    train_df, val_df, test_df = dataset.split_by_speaker(df)
    
    train_spks = set(train_df["client_id"].unique())
    val_spks = set(val_df["client_id"].unique())
    test_spks = set(test_df["client_id"].unique())
    
    # Assert disjointness
    leakage_train_val = train_spks.intersection(val_spks)
    leakage_train_test = train_spks.intersection(test_spks)
    leakage_val_test = val_spks.intersection(test_spks)
    
    assert len(leakage_train_val) == 0, f"Leakage between Train and Val: {leakage_train_val}"
    assert len(leakage_train_test) == 0, f"Leakage between Train and Test: {leakage_train_test}"
    assert len(leakage_val_test) == 0, f"Leakage between Val and Test: {leakage_val_test}"
    print("  [PASSED] Speaker splitting unit test (No Leakage detected).")

def test_model_structure():
    print("Testing model structure...")
    dummy_input_shape = (501, 64, 1)
    keras_model = model.build_cnn_lstm_model(dummy_input_shape)
    
    # Assert output shape
    assert keras_model.output_shape == (None, 1), f"Expected output shape (None, 1), got {keras_model.output_shape}"
    print("  [PASSED] Model structure unit test.")

def test_dry_run_training():
    print("Testing dry run training loop...")
    # Make config run extremely lightweight
    original_epochs = config.EPOCHS
    original_batch = config.BATCH_SIZE
    original_subset = config.SUBSET_FRACTION
    
    config.EPOCHS = 1
    config.BATCH_SIZE = 4
    config.SUBSET_FRACTION = 0.1
    
    try:
        # Load small mock metadata
        df = dataset.load_and_preprocess_metadata(config.DATA_DIR)
        train_df, val_df, test_df = dataset.split_by_speaker(df)
        
        # Subsample to a few records
        train_df = train_df.head(4).copy()
        val_df = val_df.head(2).copy()
        
        train_gen = dataset.VoiceDatasetGenerator(train_df, batch_size=2, augment=True, shuffle=True)
        val_gen = dataset.VoiceDatasetGenerator(val_df, batch_size=2, augment=False, shuffle=False)
        
        # Build model
        dummy_model = model.build_cnn_lstm_model(train_gen.input_shape)
        
        # Train for 1 epoch
        print("  Running 1 epoch dry-run training...")
        dummy_model.fit(
            train_gen,
            validation_data=val_gen,
            epochs=1,
            verbose=1
        )
        print("  [PASSED] Dry-run training integration test.")
    finally:
        # Restore configuration values
        config.EPOCHS = original_epochs
        config.BATCH_SIZE = original_batch
        config.SUBSET_FRACTION = original_subset

def main():
    print("=========================================")
    print("      Running Pipeline Unit Tests        ")
    print("=========================================")
    test_preprocessing()
    test_feature_extraction()
    test_data_leakage()
    test_model_structure()
    test_dry_run_training()
    print("=========================================")
    print("      ALL TESTS PASSED SUCCESSFULLY!    ")
    print("=========================================")

if __name__ == "__main__":
    main()
