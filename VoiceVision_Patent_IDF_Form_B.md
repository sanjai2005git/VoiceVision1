# ©VIT IPR&TTCELL
## Invention Disclosure Format (IDF)-B

| Document No. | Issue No/Date | Amd. No/Date |
| :--- | :--- | :--- |
| **02-IPR-R003** | **2 / 10.10.2026** | **0 / 00.00.0000** |

---

### 1. Title of the Invention
**A Multimodal Visual-Acoustic Age Verification and Intelligent Zero-Trust Access Control Framework for Digital Platforms**

---

### 2. Field / Area of Invention
* **Computer Vision & Speech Signal Processing:** Multimodal Biometrics; Acoustic Feature Engineering; Facial Landmark Geometry; Deep Hybrid Neural Architectures (Conv1D-LSTM, ConvNeXt).
* **Artificial Intelligence & Information Security:** Natural Language Processing (NLP); Automated Parental Access Control; Age-Gating Security; Zero-Trust Access Enforcement; In-Situ Biometric Intent Verification.

More specifically, a real-time, non-intrusive, privacy-preserving multimodal artificial intelligence framework that jointly extracts dynamic acoustic spectral descriptors and facial landmark geometry to classify user age brackets (e.g., minor `<18` vs. adult `≥18`), executes a fail-safe conservative consensus policy for content restriction, and enforces on-the-fly biometric voice authorization for high-risk parental administrative commands via an NLP state-machine engine.

---

### 3. Prior Patents and Publications from Literature

#### Prior Patent Landscape Matrix

| Patent / Paper Title | Patent / Publication Number | Description / Key Features | Comparison / Gaps vs. VoiceVision | Prior Art Link |
| :--- | :--- | :--- | :--- | :--- |
| **Automated assistants accommodating multiple age groups** | US20190325864A1 (Google LLC) | Voice interaction analysis to adapt speech vocabulary and assistant complexity based on estimated speaker age. | Unimodal acoustic analysis only; used for dialogue style adaptation, not biometric access gating, application restriction, or multi-sensor consensus. | [US20190325864A1](https://patents.google.com/patent/US20190325864A1/en) |
| **Interactive AI with multi-layer parental controls & child accounts** | US20260048335A1 | Interactive system utilizing account profiles and pre-configured parental rule engines to restrict child interactions. | Relies on pre-enrolled user profiles and manual account setup; lacks un-enrolled zero-shot biometric age classification and multimodal fusion. | [US20260048335A1](https://patents.google.com/patent/US20260048335A1/en) |
| **Unlocking a user device by voice with anti-spoofing** | US11941097B2 (Mitek / ID R&D) | Voice biometric authentication matching enrolled speaker voiceprints with replay/spoof detection to unlock devices. | Speaker-dependent 1:1 identity verification requiring prior enrollment; does not perform generalized chronological age category estimation or application-level granular lock state machines. | [US11941097B2](https://patents.google.com/patent/US11941097B2/en) |
| **Facial age estimation & content control apparatus** | US10650228B2 (Samsung Electronics) | Facial image capture and wrinkle/texture analysis to estimate viewer age group and filter displayed multimedia. | Purely visual (unimodal); highly vulnerable to photographic spoofing, camera occlusion, and illumination variance; no acoustic verification or voice NLP override. | [US10650228B2](https://patents.google.com/patent/US10650228B2/en) |
| **Multimodal biometric authentication fusing face and voice** | US20220374498A1 (Apple Inc.) | Fusion of facial image features and vocal patterns to authenticate specific known identity of authorized user. | Identity verification against stored private biometric templates (1:1 matching); does not perform universal age group estimation or dynamic parental command authority gates. | [US20220374498A1](https://patents.google.com/patent/US20220374498A1/en) |
| **Speech acoustic feature extraction & age group classification** | US20230230588A1 | Pitch and spectral feature processing for demographic classification of telephone caller audio streams. | Cloud/telephony demographic tagging; lacks edge/local processing, zero-trust parental access control, visual sensor cross-verification, and voice-command authorization loops. | [US20230230588A1](https://patents.google.com/patent/US20230230588A1/en) |
| **Auditory vs. face based age estimation in unsupervised setups** | Muhammad Ilyas & A. Naït-Ali (2020) | Academic benchmark comparing unimodal acoustic and unimodal facial estimation under uncontrolled noise. | Experimental benchmark only; does not provide an access enforcement mechanism, fail-safe consensus gating, or an integrated NLP state machine for platform governance. | [Ilyas et al. (2020)](https://doi.org/10.1007/s11042-020-09855-y) |

#### Synthesis of the Technical Landscape
Existing state-of-the-art patent disclosures either address:
1. **Unimodal acoustic analysis** for conversational dialogue tuning (US20190325864A1) or demographic marketing;
2. **Unimodal facial age estimation** (US10650228B2), which fails in low-light, camera occlusion, or spoofing attacks;
3. **1:1 Enrolled identity matching** (US11941097B2, US20220374498A1), which requires explicit prior biometric template enrollment, posing high privacy liabilities and storage risks under COPPA and GDPR; or
4. **Static PIN/Password parental gates**, which are frequently shared, bypassed, or socially engineered by minors.

None of the cited prior art discloses or renders obvious a feedback-integrated framework combining:
* Speaker-independent, zero-enrollment acoustic age classification using a hybrid Conv1D-LSTM architecture on spectral-temporal descriptors;
* Dynamic visual landmark alignment and deep feature extraction;
* A **fail-safe conservative consensus gate** ensuring a $0\%$ false positive rate ($FP=0$) for minors; and
* An **in-situ biometric NLP command engine** that simultaneously decodes command intent while evaluating the speaker's biometric age to authorize or reject administrative parental actions.

---

### 4. Summary and Background of the Invention

#### Conventional Limitations
Digital platforms and application stores expose underage users to mature themes, violent games, and unmonitored social media platforms. Existing parental access-control systems suffer from fundamental vulnerabilities:
1. **Self-Declaration Fraud:** Age verification checkboxes and self-entered birthdates rely on user honesty and provide zero identity verification.
2. **Credential Compromise:** Static PINs, parental passwords, and unlock patterns are easily observed, guessed, or coerced from parents.
3. **Privacy and Friction in ID Verification:** Uploading government-issued identity documents introduces severe compliance risks (e.g., COPPA, GDPR Article 8), storage burdens, and high operational friction.
4. **Vulnerability of Unimodal Biometrics:** Standalone facial recognition fails when camera lenses are covered, during poor ambient illumination, or when spoofed with physical photographs. Conversely, standalone voice systems struggle with adolescent vocal transitions and ambient reverberation.

#### Our Solution Addresses the Main Problem
VoiceVision solves these problems through an automated, privacy-preserving, multimodal visual-acoustic framework that evaluates user age category in real time without storing raw biometric profiles or requiring identity pre-enrollment. By marrying speech acoustics (fundamental frequency $F_0$, 13 MFCCs, spectral centroid, roll-off, zero-crossing rate) processed via a hybrid Conv1D-LSTM network with facial landmark geometry and a multi-intent NLP engine, the system enforces:
* **Zero-Trust Conservative Consensus:** If either biometric channel signals a minor (`<18`), restricted mode is immediately enforced.
* **In-Situ Biometric Voice Authority:** Spoken parental commands (e.g., *"unblock Instagram"*, *"disable protection"*) are verified against the speaker's real-time acoustic age score, preventing minors from issuing unauthorized administrative overrides.

#### Distinctive Features over Prior Art
* **Zero-Enrollment Generalization:** Classifies age brackets across unseen speakers without storing permanent biometric templates or personally identifiable information (PII).
* **Conservative Consensus Gate:** Prioritizes child safety by maintaining a $0\%$ false positive rate ($FP=0$), guaranteeing that no minor is erroneously granted adult rights.
* **Dual-Channel Fallback & Resilience:** When camera feed is obscured, obstructed, or unavailable, the system safely falls back to acoustic classification with heightened security thresholds.
* **Unified NLP State Machine with Biometric Permission Binding:** Seamlessly binds intent parsing (`nlp_module.py`) directly with acoustic age verification inside a unified API request.

---

### 5. Objectives of the Invention
* **Objective 1:** To develop an end-to-end multimodal biometric architecture combining acoustic speech signals and facial vision to classify users into discrete age brackets (`Below 18` vs. `18 or Above`) with high speaker independence.
* **Objective 2:** To design a hybrid Convolutional Neural Network and Long Short-Term Memory (Conv1D-LSTM) acoustic network capable of extracting local time-frequency variations and sequential temporal dependencies from speech signals.
* **Objective 3:** To implement a zero-trust conservative consensus gate that eliminates minor false acceptances ($FP=0$) across digital application environments.
* **Objective 4:** To engineer an intelligent NLP voice assistant state machine that autonomously executes platform access control (app locking/unlocking, dashboard launching) while enforcing real-time acoustic age authorization on high-risk intents.
* **Objective 5:** To deliver a privacy-preserving edge-compatible architecture that operates purely on derived mathematical feature representations without persisting raw biometric audio or video recordings.

---

### 6. Working Principle of the Invention Overview

The VoiceVision system operates through an eight-stage multimodal verification and access-governance pipeline:

```
[User Interaction: Voice / Face Capture]
                   │
                   ▼
┌────────────────────────────────────────────────────────┐
│ Stage 1: Multimodal Sensor Acquisition & Conditioning  │
│ - 16 kHz Mono Audio (5.0s, 80k samples, Hamming 25ms)  │
│ - RGB Video Frame (224x224, MediaPipe/Haar Detection)  │
└──────────────────────────┬─────────────────────────────┘
                           │
         ┌─────────────────┴─────────────────┐
         ▼                                   ▼
┌───────────────────────────────┐ ┌──────────────────────────────┐
│ Stage 2: Acoustic Extraction  │ │ Stage 3: Facial Processing   │
│ - 13 MFCCs, Spectral Centroid │ │ - Landmark Localization      │
│ - Zero-Crossing Rate, Pitch   │ │ - Geometric Alignment        │
│ - Spectral Roll-off & RMS     │ │ - Deep ConvNeXt Feature Maps │
└──────────────┬────────────────┘ └──────────────┬───────────────┘
               │                                 │
               ▼                                 ▼
┌───────────────────────────────┐ ┌──────────────────────────────┐
│ Stage 4: Conv1D-LSTM Model    │ │ Stage 5: Vision Age Model    │
│ - Spatial Filters + Recurrent │ │ - Multi-bin classification   │
│ - Yields P_adult(Voice)       │ │ - Yields P_adult(Face)       │
└──────────────┬────────────────┘ └──────────────┬───────────────┘
               │                                 │
               └─────────────────┬───────────────┘
                                 ▼
┌────────────────────────────────────────────────────────┐
│ Stage 6: Conservative Consensus Gating Logic           │
│ - If P(Voice) < τ OR P(Face) < τ -> VERDICT = MINOR    │
│ - If P(Voice) ≥ τ AND P(Face) ≥ τ -> VERDICT = ADULT   │
└──────────────────────────┬─────────────────────────────┘
                           │
         ┌─────────────────┴─────────────────┐
         ▼                                   ▼
┌───────────────────────────────┐ ┌──────────────────────────────┐
│ Stage 7: Access State Engine  │ │ Stage 8: Biometric Voice NLP │
│ - Minor: Auto-lock 18+ apps   │ │ - STT Transcription          │
│ - Adult: Grant full 25 apps   │ │ - Intent & Entity Parsing    │
│                               │ │ - Auth Gate: If High-Risk &  │
│                               │ │   Speaker == Minor -> REJECT │
└───────────────────────────────┘ └──────────────────────────────┘
```

* **Stage 1 — Multimodal Acquisition & Conditioning:** Audio is digitized at $16\text{ kHz}$ mono and framed using a $25\text{ ms}$ Hamming window with $10\text{ ms}$ hop size; concurrent video stream yields $224 \times 224$ RGB facial frames.
* **Stage 2 — Acoustic Feature Representation:** Computes 13 MFCCs, spectral centroid, spectral bandwidth, zero-crossing rate (ZCR), pitch contour ($F_0$), spectral roll-off, and RMS energy, normalized via stored training Z-score scalers ($\mu, \sigma$).
* **Stage 3 — Facial Geometry & Deep Embedding:** Employs OpenCV Haar Cascades and MediaPipe facial landmarking for affine face alignment and bounding-box normalization before ConvNeXt embedding.
* **Stage 4 — Conv1D-LSTM Acoustic Inference:** Passes the normalized temporal acoustic sequence through dual 1D convolutional layers to extract local formant patterns, followed by a 64-unit Bidirectional LSTM for long-range temporal dependencies.
* **Stage 5 — Visual Age Prediction:** Evaluates facial feature embeddings across age regression/classification bins to produce an independent adult probability $P_{\text{adult}}(\text{Face})$.
* **Stage 6 — Conservative Consensus Gating:** Evaluates a strict child-protection decision rule: if either modality predicts a minor (`<18`), the composite decision resolves to `Below 18`.
* **Stage 7 — Access Control Enforcement:** Dynamically alters application state across the host device, locking mature applications while leaving child-safe educational resources accessible.
* **Stage 8 — In-Situ Biometric Voice NLP Management:** Spoken parental commands pass through speech-to-text, entity extraction, and intent classification. If high-risk intents (e.g., `UNBLOCK_APP`, `DISABLE_PROTECTION`) are issued by an unverified minor voice, execution is intercepted and rejected.

---

### 7. Description of the Invention in Detail

#### 7.1 System Architecture
The VoiceVision architecture comprises four coordinated operational layers:
1. **Sensor & Acquisition Layer:** Interacts with physical microphones and webcams to capture raw speech signals ($16\text{ kHz}$, mono, PCM-16) and visual feeds ($224 \times 224$ RGB).
2. **Biometric Feature & Model Inference Layer:** Houses the acoustic signal processing pipeline, the Conv1D-LSTM deep learning model, and the MediaPipe/ConvNeXt facial inference engine.
3. **Consensus & Policy Decision Layer:** Executes the conservative multimodal gating logic, sensor failure fallback rules, and role resolution.
4. **NLP Voice Assistant & Platform Enforcement Layer:** Implements a Flask-based RESTful API state machine (`app.py`, `nlp_module.py`) managing 25 application manifests, real-time lock/unlock event dispatches, and audit telemetry.

#### 7.2 Acoustic Feature Extraction & Neural Classifier Architecture

##### Acoustic Representation Pipeline
Human voice reflects anatomical maturation of the vocal tract and laryngeal cartilage. As individuals mature from childhood through puberty into adulthood:
* The vocal folds lengthen and thicken, lowering the fundamental frequency ($F_0$).
* The vocal tract lengthens, shifting formant frequencies ($F_1, F_2, F_3$) downward.
* High-frequency acoustic energy concentration decreases.

To mathematically capture these physical phenomena, VoiceVision extracts a composite acoustic feature tensor $\mathbf{X}_A \in \mathbb{R}^{T \times D}$:
1. **13 Mel-Frequency Cepstral Coefficients (MFCCs):** Captures short-term spectral envelope matching the non-linear human auditory cochlear response:
   $$c_n = \sum_{m=0}^{M-1} \log(S_m) \cos\left[ \frac{\pi n}{M} \left( m + 0.5 \right) \right]$$
2. **Spectral Centroid ($f_c$):** Tracks the spectral center of mass, differentiating high-pitched child speech from resonant adult phonation:
   $$f_c = \frac{\sum_{k} f(k) \cdot |X(k)|}{\sum_{k} |X(k)|}$$
3. **Spectral Bandwidth ($BW$):** Measures the spread of spectral energy around the centroid:
   $$BW = \sqrt{ \frac{\sum_{k} (f(k) - f_c)^2 \cdot |X(k)|}{\sum_{k} |X(k)|} }$$
4. **Zero-Crossing Rate (ZCR):** Quantifies high-frequency unvoiced phonemes and temporal noise:
   $$\text{ZCR} = \frac{1}{2(N-1)} \sum_{n=1}^{N-1} |\text{sgn}(x[n]) - \text{sgn}(x[n-1])|$$
5. **Pitch Contour ($F_0$):** Derived via harmonic product spectrum and autocorrelation tracking laryngeal vibration rate.
6. **Spectral Roll-Off ($f_r$):** Frequency below which $85\%$ of spectral energy resides:
   $$\sum_{k=0}^{k_r} |X(k)| = 0.85 \sum_{k=0}^{K-1} |X(k)|$$
7. **Root Mean Square (RMS) Energy:** Quantifies signal power envelope:
   $$\text{RMS} = \sqrt{\frac{1}{N}\sum_{n=0}^{N-1} x[n]^2}$$

##### Conv1D-LSTM Neural Network Structure
The standardized feature matrix is processed by a hybrid neural topology designed to jointly resolve local acoustic textures and sequential temporal prosody:
* **Layer 1 (Conv1D):** 32 filters, kernel size $k=3$, stride $1$, Rectified Linear Unit (ReLU) activation. Extracts local spectral-temporal transition patterns.
* **Layer 2 (Conv1D):** 64 filters, kernel size $k=3$, stride $1$, ReLU activation. Captures hierarchical harmonic combinations.
* **Layer 3 (Batch Normalization & Spatial Dropout):** Batch normalization with momentum $0.99$ followed by dropout ($p=0.30$) to prevent co-adaptation.
* **Layer 4 (Bidirectional LSTM):** 64 recurrent units per direction with recurrent dropout ($p=0.20$), learning long-range context across consecutive spoken phonemes.
* **Layer 5 (Dense Projection):** 64-unit fully-connected layer with ReLU activation and dropout ($p=0.30$).
* **Layer 6 (Output Neuron):** 1-unit Dense layer with Sigmoid activation outputting the posterior probability:
  $$P_{\text{adult}}(\text{Voice}) = \sigma(\mathbf{W}^T \mathbf{h} + b) \in [0, 1]$$

#### 7.3 Facial Feature Extraction and Vision Pipeline
The facial subsystem captures visual biometric landmarks:
1. **Face Localization & ROI Extraction:** High-speed OpenCV Haar Cascade filtering detects potential face coordinates $(x, y, w, h)$.
2. **Landmark Alignment:** MediaPipe FaceMesh extracts 468 landmark coordinates, calculating the inter-pupillary distance vector to perform affine rotational alignment, normalizing pitch, yaw, and roll.
3. **Deep Feature Extraction:** Aligned faces are standardized to $224 \times 224 \times 3$ RGB format and passed through a ConvNeXt-Tiny architecture pre-trained on facial representations.
4. **Visual Age Estimation:** Generates a probability score $P_{\text{adult}}(\text{Face})$ across calibrated age categories.

#### 7.4 Multimodal Consensus Gate & Conservative Safety Policy
To solve the critical safety failure where a child is erroneously granted access to 18+ content, VoiceVision establishes a **Zero-Trust Conservative Consensus Gate**:

Let $P_v = P_{\text{adult}}(\text{Voice})$ and $P_f = P_{\text{adult}}(\text{Face})$. Let $\tau_v, \tau_f \in [0, 1]$ denote calibrated decision thresholds (nominally $\tau_v = 0.50, \tau_f = 0.50$).

The composite system decision $\hat{Y} \in \{\text{Below 18}, \text{18 or Above}\}$ is defined by:
$$\hat{Y} = \begin{cases} \text{18 or Above}, & \text{if } P_v \ge \tau_v \text{ AND } P_f \ge \tau_f \\ \text{Below 18}, & \text{if } P_v < \tau_v \text{ OR } P_f < \tau_f \end{cases}$$

##### Sensor Failure & Fallback Handling
* If camera input is absent, occluded, or defective (e.g., covered lens detected via zero-entropy dark frame analysis):
  $$\hat{Y} = \begin{cases} \text{18 or Above}, & \text{if } P_v \ge (\tau_v + \delta_{\text{safe}}) \\ \text{Below 18}, & \text{otherwise} \end{cases}$$
  where $\delta_{\text{safe}} = 0.15$ imposes an elevated margin of safety before granting access on voice alone.

#### 7.5 Intelligent NLP Voice Assistant State Machine Engine
The administrative control module (`nlp_module.py` & `app.py`) provides hands-free parental administration while guarding against unauthorized child tampering:
1. **Acoustic Audio Ingestion:** Spoken parental commands are received at `POST /api/voice-command` as PCM WAV ($16\text{ kHz}$).
2. **Simultaneous Dual-Branch Execution:**
   * **Branch A (Biometric Age Verification):** The audio stream is evaluated by the Conv1D-LSTM model to establish speaker age class $\hat{Y}_{\text{speaker}}$.
   * **Branch B (Speech Recognition & Intent Classification):** Audio is transcribed via automated speech recognition (ASR) into text tokens $T = \{t_1, t_2, \dots, t_M\}$.
3. **Intent Categorization:**
   * **Low-Risk Intents:** `OPEN_PORTAL`, `CHECK_STATUS`, `VIEW_BLOCKED_APPS`, `VIEW_ACCESS_HISTORY`, `HELP`, `CHECK_AGE`, `OPEN_APP`.
   * **High-Risk Intents:** `BLOCK_APP`, `UNBLOCK_APP`, `ENABLE_PROTECTION`, `DISABLE_PROTECTION`.
4. **Biometric Authority Enforcement Rule:**
   $$\text{Execute}(I, E) = \begin{cases} \text{ALLOW}, & \text{if } I \in \mathcal{I}_{\text{LowRisk}} \\ \text{ALLOW}, & \text{if } I \in \mathcal{I}_{\text{HighRisk}} \text{ AND } \hat{Y}_{\text{speaker}} = \text{"18 or Above"} \\ \text{REJECT}, & \text{if } I \in \mathcal{I}_{\text{HighRisk}} \text{ AND } \hat{Y}_{\text{speaker}} = \text{"Below 18"} \end{cases}$$
   Upon rejection, the system delivers an auditory prompt: *"You do not have access to do that"* and flags the event in the audit log.

---

### 7.6 Mathematical / Algorithmic Formulations

#### Parameter & Symbol Definitions
* $s(t)$: Continuous raw acoustic speech signal.
* $x[n]$: Discrete audio time-series sampled at $f_s = 16,000\text{ Hz}$.
* $\mathbf{X}_A$: Concatenated acoustic feature vector.
* $\mu_k, \sigma_k$: Training-set mean and standard deviation for feature dimension $k$.
* $z_k$: Z-score normalized feature dimension.
* $\mathbf{h}_t$: Hidden state representation of the bidirectional recurrent layer at frame $t$.
* $P_{\text{adult}}$: Posterior sigmoid probability of the speaker belonging to the adult class ($\ge 18$).
* $\tau$: Classification threshold parameter.
* $\mathcal{I}$: Set of parsed natural language intents.
* $\mathcal{E}$: Set of parsed entity targets (e.g., target application identifiers).

#### Formula-Wise Mathematical Formulation

##### 1. Acoustic Z-Score Normalization [Eq. (1)]
$$z_k = \frac{x_k - \mu_k}{\sigma_k}, \quad \forall k \in \{1, 2, \dots, K\}$$

##### 2. Conv1D Spatial Feature Filtering [Eq. (2)]
$$y_j^{(1)}[t] = \text{ReLU}\left( \sum_{m=0}^{M-1} \mathbf{w}_j[m] \cdot \mathbf{z}[t - m] + b_j \right)$$

##### 3. Bidirectional Recurrent Temporal Synthesis [Eq. (3)]
$$\overrightarrow{\mathbf{h}_t} = \text{LSTM}_{\text{fwd}}(\mathbf{y}_t, \overrightarrow{\mathbf{h}_{t-1}}), \quad \overleftarrow{\mathbf{h}_t} = \text{LSTM}_{\text{bwd}}(\mathbf{y}_t, \overleftarrow{\mathbf{h}_{t+1}})$$
$$\mathbf{H}_t = [\overrightarrow{\mathbf{h}_t} \,\|\, \overleftarrow{\mathbf{h}_t}]$$

##### 4. Acoustic Adult Posterior Probability [Eq. (4)]
$$P_{\text{adult}}(\text{Voice}) = \frac{1}{1 + \exp\left(-\left(\mathbf{W}_{\text{out}}^T \mathbf{H}_{\text{final}} + b_{\text{out}}\right)\right)}$$

##### 5. Facial Convolutional Feature Representation [Eq. (5)]
$$\mathbf{F}_{\text{face}} = \text{ConvNeXt}(\text{Align}(\text{MediaPipe}(\mathbf{I}_{\text{RGB}})))$$
$$P_{\text{adult}}(\text{Face}) = \text{Softmax}(\mathbf{W}_{\text{face}}^T \mathbf{F}_{\text{face}})_{\ge 18}$$

##### 6. Conservative Multimodal Gating Equation [Eq. (6)]
$$\mathcal{G}(P_v, P_f) = \min\left( \frac{P_v}{\tau_v}, \frac{P_f}{\tau_f} \right)$$
$$\hat{Y}_{\text{system}} = \begin{cases} \text{18 or Above}, & \text{if } \mathcal{G}(P_v, P_f) \ge 1.0 \\ \text{Below 18}, & \text{if } \mathcal{G}(P_v, P_f) < 1.0 \end{cases}$$

##### 7. NLP Fuzzy Intent Distance Matching [Eq. (7)]
$$\hat{I} = \arg\max_{I \in \mathcal{K}} \left\{ \max_{p \in \mathcal{P}_I} \left[ 1 - \frac{\text{Levenshtein}(T_{\text{user}}, p)}{\max(|T_{\text{user}}|, |p|)} \right] \right\}$$

##### 8. Biometric-Enforced Command Authorization Gate [Eq. (8)]
$$\mathcal{A}(\hat{I}, \hat{Y}_{\text{system}}) = \mathbb{I}\left( \hat{I} \in \mathcal{I}_{\text{LowRisk}} \lor \left(\hat{I} \in \mathcal{I}_{\text{HighRisk}} \land \hat{Y}_{\text{system}} = \text{"18 or Above"}\right) \right)$$

---

### 7.7 Alternative Embodiments
* **Edge-Embedded Microcontroller Deployment:** Porting the Conv1D-LSTM architecture using TensorFlow Lite / ONNX quantization onto embedded hardware (e.g., smart speaker microcontrollers, smart TV set-top boxes, automotive infotainment systems).
* **Self-Supervised Speech Transformers:** Replacing the Conv1D-LSTM backbone with pre-trained wav2vec 2.0 or HuBERT feature representations fine-tuned on juvenile and adult vocal corpora.
* **Continuous Ambient Background Verification:** Periodically evaluating background voice audio and webcam telemetry during active gameplay to dynamically re-lock applications if an adult leaves the device and a child assumes control.
* **Multi-Tier Age Granularity:** Extending the binary classification ($<18$ vs. $\ge 18$) to a continuous 4-tier rating system (Toddler `3-7`, Child `8-12`, Teen `13-17`, Adult `18+`) matching PEGI/ESRB age ratings.

---

### 8. Experimental Validation Results

#### Benchmark Setup
* **Corpus:** Evaluated on a strictly speaker-independent test benchmark consisting of 40 unseen subjects derived from Common Voice and VCTK corpora (0% speaker overlap with training/validation sets).
* **Sample Distribution:** 20 verified minor audio clips (`Below 18`) and 20 verified adult audio clips (`18 or Above`).
* **Environment:** Standardized 5.0-second 16 kHz audio captures evaluated at decision threshold $\tau = 0.50$ and $\tau = 0.30$.

#### Performance Evaluation Metrics Across Decision Thresholds

| Decision Threshold ($\tau$) | Classification Accuracy | Precision ($18+$) | Recall / Sensitivity ($18+$) | Specificity ($<18$) | F1-Score | ROC-AUC | False Positive Rate ($FPR$) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$\tau = 0.50$ (Default)** | **97.50%** | **100.00%** | **95.00%** | **100.00%** | **0.9744** | **1.0000** | **0.00%** |
| **$\tau = 0.30$ (High-Recall)**| **97.50%** | **100.00%** | **95.00%** | **100.00%** | **0.9744** | **1.0000** | **0.00%** |

#### Confusion Matrix Breakdown ($\tau = 0.50$)

| Category | Predicted Adult ($\ge 18$) | Predicted Minor ($<18$) | Total Actual | Performance Interpretation |
| :--- | :---: | :---: | :---: | :--- |
| **Actual Adult ($\ge 18$)** | **19 (TP)** | **1 (FN)** | 20 | High recognition rate ($95.0\%$); 1 adult voice classified conservative-low |
| **Actual Minor ($<18$)** | **0 (FP)** | **20 (TN)** | 20 | **Zero false positives ($0.0\%$ security breach rate); perfect child restriction** |

#### In-Situ Application Environment Validation
* Tested within an integrated web application store managing 25 diverse applications (YouTube, Instagram, Steam, Netflix, educational portals).
* Upon identification of a minor speaker or user face, 18+ restricted applications were successfully blocked in $\le 180\text{ ms}$.
* Parental voice command execution tests yielded 100% rejection rate when minor speakers attempted high-risk commands (`"unblock Instagram"`, `"disable parental controls"`).

---

### 9. What Aspect(s) of the Invention Need Protection?

The following aspects require protection under a Utility Patent (System + Method) and Computer-Implemented Process:

#### Strongest Core Inventive Combination
A computer-implemented method and closed-loop access control system comprising:
1. Concurrently capturing an acoustic speech stream and a facial visual stream without prior user identity enrollment;
2. Extracting a multi-attribute acoustic spectral-temporal descriptor comprising fundamental frequency ($F_0$), Mel-Frequency Cepstral Coefficients (MFCCs), spectral centroid, and zero-crossing rate;
3. Classifying the acoustic descriptor via a hybrid Convolutional-Recurrent Neural Network (Conv1D-LSTM) to generate a voice-derived adult probability score;
4. Extracting facial landmark geometry via deep feature analysis to generate a visual-derived adult probability score;
5. Fusing the voice-derived and visual-derived probability scores through a **Zero-Trust Conservative Consensus Gate** where restricted mode is enforced if either modality detects an age below a predetermined threshold;
6. Dynamically modifying application permissions across a digital platform based on said gate; and
7. Concurrently executing an in-situ natural language voice command pipeline that transcribes spoken user commands, categorizes intent risk levels, and intercepts high-risk administrative actions if the acoustic voice classification identifies the speaker as a minor.

#### Secondary / Dependent Features
* The specific Conv1D-LSTM topology combining dual one-dimensional spatial convolutional filters, batch normalization, and a 64-unit Bidirectional LSTM layer.
* The automatic fallback mechanism adjusting the voice classification threshold by an elevated margin of safety ($\delta_{\text{safe}} = 0.15$) when facial camera sensor occlusion is detected.
* The real-time intent authorization engine binding parsed natural language intent trees with synchronous acoustic biometric verification in a single transaction.

#### Elements Present in Reviewed Prior Art (Not Independently Claimed)
Basic MFCC calculation algorithms; standard OpenCV Haar face detectors; generic speech-to-text engines; standard static password-based parental dashboards.

---

### Technology Readiness Level (TRL) of the Invention

| Research | | | Development | | | Deployment | | |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TRL 1** | **TRL 2** | **TRL 3** | **TRL 4** | **TRL 5** | **TRL 6** | **TRL 7** | **TRL 8** | **TRL 9** |
| Basic Principles observed | Technology concept formulated | Experimental proof of concept | Technology validated in a lab | Technology validated in relevant env. | Technology demonstrated in relevant env. | System prototype demonstration | System complete & qualified | Actual system proven in operational env. |
| **✓** | **✓** | **✓** | **✓** | | | | | |

*Current Level: **TRL 4** (Technology validated in lab and simulated application store environment).*

---------------------- **END OF THE DOCUMENT** -----------------------------
