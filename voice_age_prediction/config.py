import os

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "saved_models")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# --- Dataset Download Config ---
# To download programmatically, set your Mozilla API key or pass it via MOZILLA_API_KEY environment variable.
MOZILLA_API_KEY = os.getenv("MOZILLA_API_KEY", "f0695ae51539002bdffa64e52596671ae13c67516e1a3ee810a0403c1f973fde")
DATASET_ID = "cmqim2hn800ssnr07gvmpcnwu"
# Local path to already downloaded .tar.gz (if available)
LOCAL_TAR_PATH = None

# For quick pipeline dry-run testing, we can limit the training dataset to a fraction (e.g., 0.05). Set to None for full run.
SUBSET_FRACTION = None  # Set to None to use 100% of the dataset

# --- Audio Preprocessing ---
SAMPLING_RATE = 16000     # 16 kHz
AUDIO_DURATION = 5        # 5 seconds
MAX_AUDIO_SAMPLES = SAMPLING_RATE * AUDIO_DURATION  # 80,000 samples

# --- Feature Extraction (STFT & Mel Spectrogram) ---
FFT_SIZE = 512            # FFT window size
WINDOW_LENGTH = 400       # Window length (25 ms at 16kHz)
HOP_LENGTH = 160          # Hop length (10 ms at 16kHz)
MEL_BINS = 64             # Number of mel filter bands (can be 64 or 80)
USE_MFCC = False          # Use Mel Spectrogram as default. Set to True to run the MFCC experiment.

# --- Model Hyperparameters ---
BATCH_SIZE = 8
LEARNING_RATE = 0.01
EPOCHS = 30
DROPOUT = 0.3
CNN_FILTERS = [32, 64, 128]
LSTM_UNITS = 64

# --- Feature Pipeline Choice ---
USE_ENGINEERED_FEATURES = True

# --- Inference Config ---
DEFAULT_THRESHOLD = 0.5   # Initial age probability threshold
