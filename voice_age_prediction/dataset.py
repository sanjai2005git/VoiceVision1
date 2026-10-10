import os
import tarfile
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm
import soundfile as sf
import tensorflow as tf
from tensorflow import keras

import config
import preprocessing
import features

def download_dataset(api_key=config.MOZILLA_API_KEY, dataset_id=config.DATASET_ID, dest_dir=config.DATA_DIR):
    """
    Downloads and extracts the Mozilla Common Voice dataset using the Mozilla Data Collective API.
    """
    tar_path = os.path.join(dest_dir, f"common-voice-{dataset_id}.tar.gz")
    
    # Check if extraction was already done
    # Standard Common Voice directories have tsv files in the extracted folders
    tsv_files = [f for f in os.listdir(dest_dir) if f.endswith('.tsv')]
    if len(tsv_files) > 0:
        print(f"Dataset already extracted in {dest_dir}.")
        return dest_dir

    if os.path.exists(tar_path):
        print(f"Archive file found at {tar_path}. Skipping download.")
    else:
        if not api_key:
            raise ValueError("No MOZILLA_API_KEY provided. Set it in config.py or environment variables.")
        
        print(f"Requesting download URL for dataset {dataset_id}...")
        url = f"https://mozilladatacollective.com/api/datasets/{dataset_id}/download"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to get download URL: {response.status_code} - {response.text}")
            
        data = response.json()
        download_url = data.get("downloadUrl")
        if not download_url:
            raise Exception("Download URL not found in API response.")
            
        print(f"Downloading from {download_url}...")
        res = requests.get(download_url, stream=True)
        total_size = int(res.headers.get('content-length', 0))
        
        with open(tar_path, 'wb') as f, tqdm(
            desc=os.path.basename(tar_path),
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in res.iter_content(chunk_size=1024 * 1024):
                size = f.write(chunk)
                bar.update(size)
                
    print(f"Extracting {tar_path} to {dest_dir}...")
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=dest_dir)
    print("Extraction completed successfully.")
    return dest_dir

def generate_vctk_dataset(dest_dir=config.DATA_DIR, num_samples=200):
    """
    Downloads a small streamed subset of VCTK from Hugging Face and builds a dataset:
    - Half the samples are saved as-is (Adults / 18 or Above).
    - The other half are pitch-shifted up by +5 semitones to simulate children (Below 18).
    - Writes audio files and validated.tsv metadata.
    """
    print(f"Building VCTK-based dataset ({num_samples} samples) from Hugging Face...")
    clips_dir = os.path.join(dest_dir, "clips")
    os.makedirs(clips_dir, exist_ok=True)
    
    import io
    import soundfile as sf
    import librosa
    from datasets import load_dataset, Audio
    
    try:
        # Load saeedzou/vctk-16khz in streaming mode to keep it extremely lightweight
        ds = load_dataset("saeedzou/vctk-16khz", split="train", streaming=True)
        # Disable automatic audio decoding to decode with soundfile (bypasses torchcodec)
        ds = ds.cast_column("audio", Audio(decode=False))
        
        iterator = iter(ds)
        metadata = []
        speaker_counts = {}
        saved_count = 0
        max_samples_per_speaker = 20
        
        while saved_count < num_samples:
            try:
                item = next(iterator)
            except StopIteration:
                print("Hugging Face stream ended early.")
                break
                
            spk = item.get("speaker_id", "unknown")
            # If we already have enough samples for this speaker, skip to ensure speaker diversity
            if speaker_counts.get(spk, 0) >= max_samples_per_speaker:
                continue
                
            audio_dict = item["audio"]
            audio_bytes = audio_dict.get("bytes")
            
            if audio_bytes is None:
                continue
                
            # Decode using soundfile
            waveform, sr = sf.read(io.BytesIO(audio_bytes))
            
            # Resample if not 16000
            if sr != 16000:
                waveform = librosa.resample(waveform, orig_sr=sr, target_sr=16000)
                sr = 16000
                
            is_child = (saved_count % 2 == 1)
            
            if is_child:
                filename = f"vctk_child_{saved_count:04d}.wav"
                age = "teens"  # Mapped to Below 18
                # Pitch-shift by +5 semitones to simulate child voice
                waveform = librosa.effects.pitch_shift(waveform, sr=sr, n_steps=5)
            else:
                filename = f"vctk_adult_{saved_count:04d}.wav"
                # VCTK speakers are adults, we map their age to twenties/thirties/etc.
                vctk_age = item.get("age", 23)
                if isinstance(vctk_age, int):
                    age = str(vctk_age)
                else:
                    age = "twenties"
                    
            filepath = os.path.join(clips_dir, filename)
            sf.write(filepath, waveform, sr)
            
            metadata.append({
                "client_id": spk,
                "path": filename,
                "age": age,
                "locale": "en",
                "sentence": item.get("text", "This is a VCTK sentence.")
            })
            speaker_counts[spk] = speaker_counts.get(spk, 0) + 1
            saved_count += 1
            
            if saved_count % 20 == 0:
                print(f"  Processed {saved_count}/{num_samples} samples (Speakers found: {len(speaker_counts)})...")
                
        df = pd.DataFrame(metadata)
        tsv_path = os.path.join(dest_dir, "validated.tsv")
        df.to_csv(tsv_path, sep="\t", index=False)
        print(f"Successfully generated VCTK dataset in {clips_dir} and metadata at {tsv_path}.")
        
    except Exception as e:
        print(f"Error building VCTK dataset: {e}")
        raise e

def load_and_preprocess_metadata(data_dir=config.DATA_DIR):
    """
    Loads metadata (validated.tsv), filters for English, processes age labels,
    removes invalid/missing ages, and returns cleaned DataFrame.
    """
    tsv_path = os.path.join(data_dir, "validated.tsv")
    
    # Check if file exists. If not, try nested directory search or generate mock
    if not os.path.exists(tsv_path):
        # Look for validated.tsv inside subdirectories (in case of nested extraction)
        found = False
        for root, dirs, files in os.walk(data_dir):
            if "validated.tsv" in files:
                tsv_path = os.path.join(root, "validated.tsv")
                # Update config.DATA_DIR to this folder
                config.DATA_DIR = root
                found = True
                break
                
        if not found:
            generate_vctk_dataset(data_dir)
            tsv_path = os.path.join(data_dir, "validated.tsv")

    print(f"Loading metadata from {tsv_path}...")
    df = pd.read_csv(tsv_path, sep="\t")
    
    initial_count = len(df)
    
    # 1. Filter for English (locale == 'en')
    df = df[df["locale"] == "en"]
    english_count = len(df)
    removed_non_english = initial_count - english_count
    
    # 2. Check path references and fix directories if clips are nested
    clips_dir = os.path.join(os.path.dirname(tsv_path), "clips")
    df["full_audio_path"] = df["path"].apply(lambda p: os.path.join(clips_dir, p))
    
    # Drop rows where audio file does not exist
    df["exists"] = df["full_audio_path"].apply(os.path.exists)
    df = df[df["exists"]]
    exists_count = len(df)
    removed_missing_files = english_count - exists_count
    
    # 3. Clean and map ages
    # Common Voice age labels: 'teens', 'twenties', 'thirties', 'fourties', 'fifties', 'sixties', 'seventies', 'eighties', 'nineties'
    # Numeric values are also possible in custom/altered metadata versions.
    def parse_age(age_val):
        if pd.isna(age_val):
            return None
        
        age_str = str(age_val).strip().lower()
        
        # If numeric
        try:
            val = float(age_str)
            if val < 18:
                return 0 # Below 18
            else:
                return 1 # 18 or Above
        except ValueError:
            pass
            
        # If string category
        if age_str == "teens":
            return 0  # Teens (typically 13-19, mapped to Below 18 for this binary task)
        elif age_str in ["twenties", "thirties", "fourties", "forties", "fifties", "sixties", "seventies", "eighties", "nineties"]:
            return 1  # 18 or Above
            
        # Ambiguous categories
        return None

    df["label"] = df["age"].apply(parse_age)
    
    # Drop invalid/missing age rows
    cleaned_df = df[df["label"].notna()].copy()
    cleaned_df["label"] = cleaned_df["label"].astype(int)
    
    final_count = len(cleaned_df)
    removed_age = exists_count - final_count
    
    print("\n--- Dataset Filtering Statistics ---")
    print(f"Initial samples: {initial_count}")
    print(f"Removed non-English samples: {removed_non_english}")
    print(f"Removed samples with missing audio files: {removed_missing_files}")
    print(f"Removed missing/invalid/ambiguous age samples: {removed_age}")
    print(f"Final usable samples: {final_count}")
    print("-------------------------------------\n")
    
    return cleaned_df

def split_by_speaker(df, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    """
    Splits the dataset according to Speaker ID (client_id) to prevent data leakage.
    Ensures that the same speaker never appears in more than one split.
    """
    unique_speakers = list(df["client_id"].unique())
    
    # Use fixed seed for deterministic splits
    np.random.seed(42)
    np.random.shuffle(unique_speakers)
    
    n_speakers = len(unique_speakers)
    train_end = int(train_ratio * n_speakers)
    val_end = int((train_ratio + val_ratio) * n_speakers)
    
    train_speakers = set(unique_speakers[:train_end])
    val_speakers = set(unique_speakers[train_end:val_end])
    test_speakers = set(unique_speakers[val_end:])
    
    train_df = df[df["client_id"].isin(train_speakers)].copy()
    val_df = df[df["client_id"].isin(val_speakers)].copy()
    test_df = df[df["client_id"].isin(test_speakers)].copy()
    
    print("--- Speaker Split Statistics ---")
    print(f"Total Speakers: {n_speakers}")
    print(f"Train Speakers: {len(train_speakers)} ({len(train_df)} samples)")
    print(f"Val Speakers:   {len(val_speakers)} ({len(val_df)} samples)")
    print(f"Test Speakers:  {len(test_speakers)} ({len(test_df)} samples)")
    print("--------------------------------\n")
    
    return train_df, val_df, test_df

_FEATURE_MEAN = None
_FEATURE_STD = None

def get_feature_scalers(df):
    """
    Computes global scaling parameters (mean and std) over the train split.
    Uses cached values if already computed.
    """
    global _FEATURE_MEAN, _FEATURE_STD
    if _FEATURE_MEAN is not None:
        return _FEATURE_MEAN, _FEATURE_STD
        
    train_speakers_df, _, _ = split_by_speaker(df)
    X_list = []
    print("Pre-calculating feature scaling parameters on train speakers...")
    for idx, row in train_speakers_df.iterrows():
        audio_path = row["full_audio_path"]
        try:
            wave = preprocessing.preprocess_audio(audio_path)
            feat = features.extract_engineered_features(wave)
            X_list.append(feat)
        except Exception:
            pass
            
    if len(X_list) > 0:
        _FEATURE_MEAN = np.mean(X_list, axis=0)
        _FEATURE_STD = np.std(X_list, axis=0) + 1e-8
    else:
        _FEATURE_MEAN = np.zeros(32, dtype=np.float32)
        _FEATURE_STD = np.ones(32, dtype=np.float32)
    print("Feature scaling parameters calculated successfully.")
    return _FEATURE_MEAN, _FEATURE_STD

class VoiceDatasetGenerator(keras.utils.Sequence):
    """
    Custom Keras Sequence generator for loading, preprocessing, augmenting,
    and extracting features from voice recordings on-the-fly.
    """
    def __init__(self, df, batch_size=config.BATCH_SIZE, augment=False, use_mfcc=config.USE_MFCC, shuffle=True, **kwargs):
        super().__init__(**kwargs)
        self.df = df.reset_index(drop=True)
        self.batch_size = batch_size
        self.augment = augment
        self.use_mfcc = use_mfcc
        self.shuffle = shuffle
        self.indices = np.arange(len(self.df))
        
        # Pre-compute input shape from a dummy sample
        dummy_wave = np.zeros(config.SAMPLING_RATE * config.AUDIO_DURATION, dtype=np.float32)
        if getattr(config, "USE_ENGINEERED_FEATURES", False):
            dummy_feat = features.extract_engineered_features(dummy_wave)
            # Retrieve scaling parameters
            self.mean, self.std = get_feature_scalers(df)
            
            # Pre-cache all features and labels in RAM
            print("Pre-caching all engineered features in RAM...")
            self.cached_X = np.empty((len(self.df), *dummy_feat.shape), dtype=np.float32)
            self.cached_y = np.empty((len(self.df), 1), dtype=np.float32)
            for idx in range(len(self.df)):
                row = self.df.iloc[idx]
                audio_path = row["full_audio_path"]
                label = row["label"]
                try:
                    waveform = preprocessing.preprocess_audio(audio_path)
                    feat = features.extract_engineered_features(waveform)
                    feat = (feat - self.mean) / self.std
                except Exception as e:
                    print(f"Error caching {audio_path}: {e}")
                    feat = np.zeros(dummy_feat.shape, dtype=np.float32)
                self.cached_X[idx] = feat
                self.cached_y[idx] = label
            print("Pre-caching completed successfully.")
        elif self.use_mfcc:
            dummy_feat = features.extract_mfcc(dummy_wave)
        else:
            dummy_feat = features.extract_log_mel_spectrogram(dummy_wave)
        self.input_shape = dummy_feat.shape
        
        self.on_epoch_end()

    def __len__(self):
        return int(np.ceil(len(self.df) / self.batch_size))

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indices)

    def __getitem__(self, index):
        # Get batch indices
        batch_indices = self.indices[index * self.batch_size : (index + 1) * self.batch_size]
        actual_batch_size = len(batch_indices)
        
        if getattr(config, "USE_ENGINEERED_FEATURES", False):
            X = self.cached_X[batch_indices]
            y = self.cached_y[batch_indices]
            return X, y
            
        X = np.empty((actual_batch_size, *self.input_shape), dtype=np.float32)
        y = np.empty((actual_batch_size, 1), dtype=np.float32)
        
        for i, idx in enumerate(batch_indices):
            row = self.df.iloc[idx]
            audio_path = row["full_audio_path"]
            label = row["label"]
            
            try:
                # 1. Preprocess waveform
                waveform = preprocessing.preprocess_audio(audio_path)
                
                # 2. Waveform data augmentation (Train set only)
                if self.augment:
                    # Random time shift (up to 10%)
                    if np.random.random() < 0.5:
                        shift_len = int(0.1 * len(waveform))
                        shift = np.random.randint(-shift_len, shift_len)
                        waveform = np.roll(waveform, shift)
                        
                    # Add background noise (white noise)
                    if np.random.random() < 0.5:
                        noise_amp = 0.005 * np.random.uniform() * np.max(np.abs(waveform))
                        waveform = waveform + noise_amp * np.random.normal(size=waveform.shape)
                
                # 3. Extract acoustic features
                if getattr(config, "USE_ENGINEERED_FEATURES", False):
                    feat = features.extract_engineered_features(waveform)
                    feat = (feat - self.mean) / self.std
                else:
                    if self.use_mfcc:
                        feat = features.extract_mfcc(waveform)
                    else:
                        feat = features.extract_log_mel_spectrogram(waveform)
                        
                    # 4. Feature augmentation (SpecAugment)
                    if self.augment:
                        # Time masking
                        if np.random.random() < 0.5:
                            mask_width = np.random.randint(2, 10)
                            start = np.random.randint(0, feat.shape[0] - mask_width)
                            feat[start : start + mask_width, :, :] = 0.0
                            
                        # Frequency masking
                        if np.random.random() < 0.5:
                            mask_width = np.random.randint(2, 8)
                            start = np.random.randint(0, feat.shape[1] - mask_width)
                            feat[:, start : start + mask_width, :] = 0.0
                
                X[i] = feat
                y[i] = label
                
            except Exception as e:
                # Fallback for errors: use zeros
                print(f"Error loading {audio_path}: {e}")
                X[i] = np.zeros(self.input_shape, dtype=np.float32)
                y[i] = label
                
        return X, y
