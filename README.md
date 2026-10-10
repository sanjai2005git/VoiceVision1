# VoiceVision V1.0

> **A Multimodal Visual-Acoustic Age Verification and Automated Parental Access Control System**

[![Version](https://img.shields.io/badge/version-v1.0-blue.svg)](https://github.com/sanjai2005git/VoiceVision1)
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)]()

---

## 📌 Overview

**VoiceVision V1.0** is an end-to-end multimodal artificial intelligence system designed to protect minors from age-inappropriate digital media and applications. Unlike traditional age gates that rely on easily bypassed checkboxes or static PINs, VoiceVision fuses:

1. **Acoustic Voice Age Classification:** Extracts acoustic spectral features (MFCCs, spectral centroid, pitch contours, zero-crossing rate, spectral roll-off) evaluated through a hybrid Deep Convolutional Neural Network and Recurrent Architecture (CNN-LSTM).
2. **Facial Visual Age Verification:** MediaPipe Face Landmarker and OpenCV alignment for anti-spoofing and visual cross-verification.
3. **Conversational NLP State Machine Engine:** Real-time hands-free parental administration allowing authorized adults to block/unblock apps and manage access policies via voice commands.

---

## 🚀 Key Features in V1.0

- **Multimodal Age Gating:** Dual-channel acoustic and visual biometric analysis for robust `<18` vs. `≥18` age group classification.
- **Fail-Safe Conservative Consensus Policy:** Enforces restriction if either modal indicator flags an underage user or if camera occlusion is detected.
- **25 Application Control Profiles:** Preset categorization covering streaming, gaming, educational, and communication apps.
- **High-Risk Command Guard:** Voice commands like `BLOCK_APP`, `UNBLOCK_APP`, and `DISABLE_PROTECTION` strictly require biometric adult voice authorization.
- **Interactive Web Interface:** Modern web dashboard featuring live voice recording, face camera verification, and real-time state machine visualization.

---

## 🛠️ Project Structure

```text
VoiceVision/
├── voice_age_prediction/
│   ├── app.py                      # Flask application and REST API endpoints
│   ├── config.py                   # Global system and model configuration (v1.0.0)
│   ├── dataset.py                  # Audio dataset loading and batch generation
│   ├── evaluate.py                 # Evaluation metrics, confusion matrix, ROC-AUC
│   ├── features.py                 # Spectral and acoustic feature extraction
│   ├── inference.py                # Real-time voice inference pipeline
│   ├── face_inference.py           # Real-time facial landmark and vision inference
│   ├── nlp_module.py               # Natural language intent engine & state machine
│   ├── model.py                    # Deep hybrid neural network architecture
│   ├── requirements.txt            # Python dependencies
│   ├── saved_models/               # Pretrained weights (best_model.keras, scalers)
│   ├── static/                     # Web styles, UI icons, and frontend JavaScript
│   └── templates/                  # Frontend HTML templates
├── VoiceVision_Patent_IDF_Form_B.md # Invention Disclosure (Patent Document)
├── research_paper_documentation.txt# Academic research paper documentation
└── README.md                       # Project documentation
```

---

## 💻 Quick Start

### 1. Setup Environment
```bash
git clone https://github.com/sanjai2005git/VoiceVision1.git
cd VoiceVision1

python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1

pip install -r voice_age_prediction/requirements.txt
```

### 2. Run Application
```bash
cd voice_age_prediction
python app.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 📄 Patent & Research Reference
- **Invention Disclosure:** Document No. `02-IPR-R003`, Issue No. `2`
- **Citation:** Sanjay et al., *VoiceVision: Multi-Modal (Voice & Face) AI Age Verification and Automated Parental Access Control*.
