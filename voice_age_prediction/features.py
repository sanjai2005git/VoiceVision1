import numpy as np
import librosa
import config

def extract_log_mel_spectrogram(waveform, sr=config.SAMPLING_RATE, n_fft=config.FFT_SIZE,
                                hop_length=config.HOP_LENGTH, win_length=config.WINDOW_LENGTH,
                                n_mels=config.MEL_BINS):
    """
    Computes a normalized log-Mel spectrogram from a 1D waveform.
    
    Args:
        waveform (np.ndarray): 1D waveform.
        sr (int): Sampling rate.
        n_fft (int): FFT size.
        hop_length (int): Hop length.
        win_length (int): Window length.
        n_mels (int): Number of Mel bins.
        
    Returns:
        np.ndarray: Spectrogram of shape (time_steps, n_mels, 1).
    """
    # 1. Compute Mel Spectrogram
    mel_spec = librosa.feature.melspectrogram(
        y=waveform,
        sr=sr,
        n_fft=n_fft,
        hop_length=hop_length,
        win_length=win_length,
        n_mels=n_mels,
        power=2.0
    )
    
    # 2. Log Scaling (convert power to decibels)
    log_mel = librosa.power_to_db(mel_spec, ref=np.max)
    
    # 3. Normalization (Mean-Std standardization)
    mean = np.mean(log_mel)
    std = np.std(log_mel)
    normalized_log_mel = (log_mel - mean) / (std + 1e-8)
    
    # 4. Transpose to align time dimension first (TimeSteps, MelBins)
    features = normalized_log_mel.T
    
    # 5. Add channel dimension for CNN compatibility (TimeSteps, MelBins, 1)
    features = np.expand_dims(features, axis=-1)
    
    return features.astype(np.float32)

def extract_mfcc(waveform, sr=config.SAMPLING_RATE, n_mfcc=20, n_fft=config.FFT_SIZE,
                 hop_length=config.HOP_LENGTH, win_length=config.WINDOW_LENGTH):
    """
    Computes normalized MFCC features from a 1D waveform.
    
    Args:
        waveform (np.ndarray): 1D waveform.
        sr (int): Sampling rate.
        n_mfcc (int): Number of MFCC coefficients.
        n_fft (int): FFT size.
        hop_length (int): Hop length.
        win_length (int): Window length.
        
    Returns:
        np.ndarray: MFCC features of shape (time_steps, n_mfcc, 1).
    """
    # 1. Extract MFCCs
    mfccs = librosa.feature.mfcc(
        y=waveform,
        sr=sr,
        n_mfcc=n_mfcc,
        n_fft=n_fft,
        hop_length=hop_length,
        win_length=win_length
    )
    
    # 2. Normalization (Mean-Std standardization)
    mean = np.mean(mfccs)
    std = np.std(mfccs)
    normalized_mfccs = (mfccs - mean) / (std + 1e-8)
    
    # 3. Transpose to align time dimension first (TimeSteps, n_mfcc)
    features = normalized_mfccs.T
    
    # 4. Add channel dimension (TimeSteps, n_mfcc, 1)
    features = np.expand_dims(features, axis=-1)
    
    return features.astype(np.float32)

def extract_engineered_features(waveform, sr=config.SAMPLING_RATE):
    """
    Extracts a 32-dimensional robust feature vector from a 1D waveform:
    - Pitch F0 (mean, std) via YIN algorithm
    - Spectral centroid (mean, std)
    - Spectral bandwidth (mean)
    - Spectral rolloff (mean)
    - MFCC coefficients 1-13 (mean, std)
    """
    # 1. Pitch estimation (YIN)
    f0 = librosa.yin(waveform, fmin=50, fmax=500, sr=sr)
    voiced_f0 = f0[f0 > 50]
    if len(voiced_f0) > 0:
        pitch_mean = np.mean(voiced_f0)
        pitch_std = np.std(voiced_f0)
    else:
        pitch_mean = 0.0
        pitch_std = 0.0
        
    # 2. Spectral centroid
    centroid = librosa.feature.spectral_centroid(y=waveform, sr=sr)[0]
    centroid_mean = np.mean(centroid)
    centroid_std = np.std(centroid)
    
    # 3. Spectral bandwidth
    bandwidth = librosa.feature.spectral_bandwidth(y=waveform, sr=sr)[0]
    bandwidth_mean = np.mean(bandwidth)
    
    # 4. Spectral rolloff
    rolloff = librosa.feature.spectral_rolloff(y=waveform, sr=sr)[0]
    rolloff_mean = np.mean(rolloff)
    
    # 5. MFCCs (13 coefficients)
    mfccs = librosa.feature.mfcc(y=waveform, sr=sr, n_mfcc=13)
    mfccs_mean = np.mean(mfccs, axis=1)
    mfccs_std = np.std(mfccs, axis=1)
    
    feat_vector = np.concatenate([
        [pitch_mean, pitch_std, centroid_mean, centroid_std, bandwidth_mean, rolloff_mean],
        mfccs_mean,
        mfccs_std
    ])
    
    return feat_vector.astype(np.float32)

