import numpy as np
import librosa
import soundfile as sf
import config

def preprocess_audio(file_path, sr=config.SAMPLING_RATE, duration=config.AUDIO_DURATION, top_db=30):
    """
    Loads and preprocesses an audio file:
    1. Loads audio (automatically converts to mono if stereo and resamples to target rate).
    2. Normalizes the peak amplitude to [-1, 1].
    3. Removes silence based on a decibel threshold (top_db).
    4. Pads or truncates to exactly the target duration.
    
    Args:
        file_path (str): Path to the audio file.
        sr (int): Target sampling rate.
        duration (int): Target duration in seconds.
        top_db (int): Threshold in decibels for silence removal.
        
    Returns:
        np.ndarray: Preprocessed 1D float32 waveform of length (sr * duration).
    """
    # 1. Load audio (converts to mono and resamples)
    try:
        y, original_sr = librosa.load(file_path, sr=sr, mono=True)
    except Exception as e:
        raise ValueError(f"Error loading {file_path}: {e}")
    
    # If the file is empty, return zeros
    if len(y) == 0:
        return np.zeros(sr * duration, dtype=np.float32)
    
    # 2. Normalize peak amplitude
    max_val = np.max(np.abs(y))
    if max_val > 0:
        y = y / max_val
        
    # 3. Remove/reduce silence
    try:
        intervals = librosa.effects.split(y, top_db=top_db)
        if len(intervals) > 0:
            y = np.concatenate([y[start:end] for start, end in intervals])
    except Exception:
        # If splitting fails, fall back to the original normalized audio
        pass

    # 4. Pad or truncate to target duration
    target_samples = sr * duration
    if len(y) > target_samples:
        # Truncate to first target_samples
        y = y[:target_samples]
    elif len(y) < target_samples:
        # Zero-pad at the end
        y = np.pad(y, (0, target_samples - len(y)), mode='constant')
        
    return y.astype(np.float32)
