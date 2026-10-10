// --- Constants: Apps Data (25 Apps in total) ---
const APPS = [
    // Below 18 Apps (10 total)
    { id: "duolingo", name: "Duolingo", dev: "Duolingo Inc.", rating: 4.7, icon: "fa-language", iconUrl: "/static/icons/Duolingo.png", color: "#58cc02", isRestricted: false, ageLimit: "All Ages" },
    { id: "yt_kids", name: "Youtube kids", dev: "Google LLC", rating: 4.5, icon: "fa-child-reaching", iconUrl: "/static/icons/youtube-for-kids.png", color: "#ff0000", isRestricted: false, ageLimit: "All Ages" },
    { id: "sketchbook", name: "Autodesk sketchbook", dev: "Autodesk Inc.", rating: 4.6, icon: "fa-palette", iconUrl: "/static/icons/Sketchbook.png", color: "#e65100", isRestricted: false, ageLimit: "All Ages" },
    { id: "abcmouse", name: "ABC Mouse", dev: "Age of Learning", rating: 4.3, icon: "fa-computer-mouse", iconUrl: "/static/icons/ABC-mouse.png", color: "#ffd600", isRestricted: false, ageLimit: "Kids" },
    { id: "minecraft", name: "Minecraft", dev: "Mojang Studios", rating: 4.8, icon: "fa-cubes", iconUrl: "/static/icons/Minecraft.png", color: "#388e3c", isRestricted: false, ageLimit: "7+" },
    { id: "roblox", name: "Roblox", dev: "Roblox Corporation", rating: 4.4, icon: "fa-square", iconUrl: "/static/icons/Roblox.png", color: "#d32f2f", isRestricted: false, ageLimit: "12+" },
    { id: "scratch", name: "Scratch", dev: "MIT Media Lab", rating: 4.7, icon: "fa-cat", iconUrl: "/static/icons/Scratch.png", color: "#ff9800", isRestricted: false, ageLimit: "All Ages" },
    { id: "teams", name: "Microsoft Teams", dev: "Microsoft Corp.", rating: 4.4, icon: "fa-users-rectangle", iconUrl: "/static/icons/Microsoft-Teams.png", color: "#4654e1", isRestricted: false, ageLimit: "All Ages" },
    { id: "subway", name: "Subway surfers", dev: "SYBO Games", rating: 4.5, icon: "fa-person-running", iconUrl: "/static/icons/Subway-Surfers.png", color: "#ff5722", isRestricted: false, ageLimit: "9+" },
    { id: "khan", name: "Khan academy", dev: "Khan Academy", rating: 4.6, icon: "fa-graduation-cap", iconUrl: "/static/icons/Khan-Academy.png", color: "#0288d1", isRestricted: false, ageLimit: "All Ages" },

    // 18+ Apps (15 total)
    { id: "instagram", name: "Instagram", dev: "Meta Platforms", rating: 4.3, icon: "fa-instagram", iconUrl: "/static/icons/Instagram.png", color: "#e1306c", isRestricted: true, ageLimit: "18+" },
    { id: "youtube", name: "Youtube", dev: "Google LLC", rating: 4.4, icon: "fa-youtube", iconUrl: "/static/icons/Youtube.png", color: "#ff0000", isRestricted: true, ageLimit: "18+" },
    { id: "facebook", name: "facebook", dev: "Meta Platforms", rating: 4.1, icon: "fa-facebook-f", iconUrl: "/static/icons/Facebook.png", color: "#1877f2", isRestricted: true, ageLimit: "18+" },
    { id: "x", name: "X", dev: "X Corp.", rating: 4.0, icon: "fa-x-twitter", iconUrl: "/static/icons/X.png", color: "#ffffff", isRestricted: true, ageLimit: "18+" },
    { id: "telegram", name: "Telegram", dev: "Telegram FZ-LLC", rating: 4.5, icon: "fa-telegram", iconUrl: "/static/icons/telegram.png", color: "#0088cc", isRestricted: true, ageLimit: "18+" },
    { id: "reddit", name: "Reddit", dev: "Reddit Inc.", rating: 4.2, icon: "fa-reddit-alien", iconUrl: "/static/icons/reddit.png", color: "#ff4500", isRestricted: true, ageLimit: "18+" },
    { id: "discord", name: "Discord", dev: "Discord Inc.", rating: 4.5, icon: "fa-discord", iconUrl: "/static/icons/Discord.png", color: "#5865f2", isRestricted: true, ageLimit: "18+" },
    { id: "snapchat", name: "Snapchat", dev: "Snap Inc.", rating: 4.2, icon: "fa-snapchat", iconUrl: "/static/icons/Snapchat.png", color: "#ffeb3b", isRestricted: true, ageLimit: "18+" },
    { id: "fiverr", name: "Fiverr", dev: "Fiverr International", rating: 4.6, icon: "fa-handshake", iconUrl: "/static/icons/Fiverr.png", color: "#00b22d", isRestricted: true, ageLimit: "18+" },
    { id: "gpay", name: "Gpay", dev: "Google LLC", rating: 4.3, icon: "fa-credit-card", iconUrl: "/static/icons/Google pay.png", color: "#4285f4", isRestricted: true, ageLimit: "18+" },
    { id: "phonepe", name: "Phonepe", dev: "PhonePe Pvt Ltd", rating: 4.4, icon: "fa-wallet", iconUrl: "/static/icons/Phonepe.png", color: "#5f259f", isRestricted: true, ageLimit: "18+" },
    { id: "steam_chat", name: "Steam chat", dev: "Valve Corp.", rating: 4.1, icon: "fa-steam", iconUrl: "/static/icons/Stream-chat.png", color: "#171a21", isRestricted: true, ageLimit: "18+" },
    { id: "twitch", name: "Twitch", dev: "Twitch Interactive", rating: 4.5, icon: "fa-twitch", iconUrl: "/static/icons/Twitch.png", color: "#9146ff", isRestricted: true, ageLimit: "18+" },
    { id: "linkedin", name: "Linkedin", dev: "LinkedIn Corp.", rating: 4.4, icon: "fa-linkedin-in", iconUrl: "/static/icons/Linkedin.png", color: "#0077b5", isRestricted: true, ageLimit: "18+" },
    { id: "indeed", name: "Indeed", dev: "Indeed Inc.", rating: 4.3, icon: "fa-briefcase", iconUrl: "/static/icons/Indeed.png", color: "#2164f3", isRestricted: true, ageLimit: "18+" }
];

// --- Application State ---
let currentAgeGroup = "Below 18"; // default
let currentVerificationMode = "voice"; // voice or manual
let isProtectionEnabled = true;
let customBlockedApps = ["instagram", "youtube", "facebook", "x", "telegram", "reddit", "discord", "snapchat", "fiverr", "gpay", "phonepe", "steam_chat", "twitch", "linkedin", "indeed"];
const ENTITY_TO_ID = {
    "youtube kids": "yt_kids",
    "abc mouse": "abcmouse",
    "subway surfers": "subway",
    "subway": "subway",
    "khan academy": "khan",
    "steam chat": "steam_chat",
    "google pay": "gpay",
    "phone pe": "phonepe"
};
let isRecording = false;
let mediaStream = null;
let audioContext = null;
let scriptProcessor = null;
let micSource = null;
let analyserNode = null;
let recordingChunks = [];
let recordStartTime = 0;
let recordTimerInterval = null;
const RECORD_LIMIT_SEC = 5.0;

// --- DOM Elements ---
const ageStatusBadge = document.getElementById("age-status-badge");
const appsContainer = document.getElementById("apps-container");
const tabVoice = document.getElementById("tab-voice");
const tabFace = document.getElementById("tab-face");
const tabManual = document.getElementById("tab-manual");
const contentVoice = document.getElementById("content-voice");
const contentFace = document.getElementById("content-face");
const contentManual = document.getElementById("content-manual");
const btnRecord = document.getElementById("btn-record");
const btnUploadTrigger = document.getElementById("btn-upload-trigger");
const fileAudioInput = document.getElementById("file-audio-input");
const sampleSelect = document.getElementById("sample-select");
const btnPlaySample = document.getElementById("btn-play-sample");
const btnEvalSample = document.getElementById("btn-eval-sample");
const btnAgeChild = document.getElementById("btn-age-child");
const btnAgeAdult = document.getElementById("btn-age-adult");
const localAudioPlayer = document.getElementById("local-audio-player");
const canvas = document.getElementById("visualizer-canvas");
const canvasCtx = canvas.getContext("2d");
const recordTimer = document.getElementById("record-timer");
const appSearchInput = document.getElementById("app-search-input");

// Face Verification elements
const faceDropZone = document.getElementById("face-drop-zone");
const fileFaceInput = document.getElementById("file-face-input");
const btnEvalFace = document.getElementById("btn-eval-face");
const btnResetFace = document.getElementById("btn-reset-face");
const previewWrapper = document.getElementById("preview-wrapper");
const uploadedImagePreview = document.getElementById("uploaded-image-preview");
const faceCropPreviewBox = document.getElementById("face-crop-preview-box");
const croppedFacePreview = document.getElementById("cropped-face-preview");
const btnTabCamStart = document.getElementById("btn-tab-cam-start");
const btnTabCamCapture = document.getElementById("btn-tab-cam-capture");
const faceWebcamCard = document.getElementById("face-webcam-card");
const tabWebcamStream = document.getElementById("tab-webcam-stream");
const tabCaptureCanvas = document.getElementById("tab-capture-canvas");
const tabWebcamStatus = document.getElementById("tab-webcam-status");
let tabWebcamMediaStream = null;

// Wizard elements
const wizardContainer = document.getElementById("wizard-container");
const wizardStep1 = document.getElementById("wizard-step-1");
const wizardStep2 = document.getElementById("wizard-step-2");
const wizardStep3 = document.getElementById("wizard-step-3");
const dotStep1 = document.getElementById("dot-step-1");
const dotStep2 = document.getElementById("dot-step-2");
const dotStep3 = document.getElementById("dot-step-3");
const btnWizardScan = document.getElementById("btn-wizard-scan");
const btnWizardUploadFaceTrigger = document.getElementById("btn-wizard-upload-face-trigger");
const wizardFileFaceInput = document.getElementById("wizard-file-face-input");
const wizardFaceStatus = document.getElementById("wizard-face-status");
const btnWizardRecord = document.getElementById("btn-wizard-record");
const btnWizardUploadVoiceTrigger = document.getElementById("btn-wizard-upload-voice-trigger");
const wizardFileAudioInput = document.getElementById("wizard-file-audio-input");
const wizardVoiceStatus = document.getElementById("wizard-voice-status");
const webcamStream = document.getElementById("webcam-stream");
const captureCanvas = document.getElementById("capture-canvas");
const scannerPlaceholder = document.getElementById("scanner-placeholder");
const wizardVoiceTimer = document.getElementById("wizard-voice-timer");
const wizardVoiceProgressBar = document.getElementById("wizard-voice-progress-bar");
const wizardVoiceVisualizer = document.getElementById("wizard-voice-visualizer");
const wizardVoiceVisualizerCtx = wizardVoiceVisualizer.getContext("2d");
const btnWizardEnter = document.getElementById("btn-wizard-enter");

// Step 3 Result fields
const wizardResFacePill = document.getElementById("wizard-res-face-pill");
const wizardResFaceBin = document.getElementById("wizard-res-face-bin");
const wizardResFaceConf = document.getElementById("wizard-res-face-conf");
const wizardResVoicePill = document.getElementById("wizard-res-voice-pill");
const wizardResVoiceBin = document.getElementById("wizard-res-voice-bin");
const wizardResVoiceConf = document.getElementById("wizard-res-voice-conf");
const wizardVerdictBox = document.getElementById("wizard-verdict-box");
const wizardVerdictTitle = document.getElementById("wizard-verdict-title");
// Assistant Drawer elements
const btnAssistantToggle = document.getElementById("btn-assistant-toggle");
const btnAssistantClose = document.getElementById("btn-assistant-close");
const assistantDrawer = document.getElementById("assistant-drawer");
const assistantStatusDot = document.getElementById("assistant-status-dot");
const assistantStatusText = document.getElementById("assistant-status-text");
const btnAssistantRecord = document.getElementById("btn-assistant-record");
const btnAssistantUploadTrigger = document.getElementById("btn-assistant-upload-trigger");
const assistantFileInput = document.getElementById("assistant-file-input");
const assistantHint = document.getElementById("assistant-hint");
const assistantTimer = document.getElementById("assistant-timer");
const assistantVisualizer = document.getElementById("assistant-visualizer");
const assistantVisualizerCtx = assistantVisualizer.getContext("2d");

// Telemetry fields
const tTranscription = document.getElementById("t-transcription");
const tIntent = document.getElementById("t-intent");
const tEntity = document.getElementById("t-entity");
const tConfidence = document.getElementById("t-confidence");
const tVerification = document.getElementById("t-verification");
const assistantActionFeedback = document.getElementById("assistant-action-feedback");
const assistantHistoryList = document.getElementById("assistant-history-list");

// Inference fields
const inferenceResults = document.getElementById("inference-results");
const resBadgeType = document.getElementById("res-badge-type");
const resClass = document.getElementById("res-class");
const resProb = document.getElementById("res-prob");
const resConfidence = document.getElementById("res-confidence");
const resProgressIndicator = document.getElementById("res-progress-indicator");

// Modals
const modalContainer = document.getElementById("modal-container");
const appWelcomeModal = document.getElementById("app-welcome-modal");
const appRestrictedModal = document.getElementById("app-restricted-modal");

// --- Initialization ---
document.addEventListener("DOMContentLoaded", () => {
    // 1. Initialize Visualizer Canvas Size
    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);
    drawIdleVisualizer();

    // 2. Load Sample Clips
    loadSampleClips();

    // 3. Render Apps in Grid
    updateAgeCategory(currentAgeGroup);
    syncPortalState();

    // 4. Attach Event Handlers
    setupEventHandlers();
    
    // 5. Initialize Multi-Modal Wizard
    initWizard();

    // 6. Initialize Voice Assistant
    initAssistant();
});

function resizeCanvas() {
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
}

// --- Event Handlers Configuration ---
function setupEventHandlers() {
    // Tab switching
    tabVoice.addEventListener("click", () => switchTab("voice"));
    tabFace.addEventListener("click", () => switchTab("face"));
    tabManual.addEventListener("click", () => switchTab("manual"));

    // Voice record
    btnRecord.addEventListener("click", toggleRecording);
    btnUploadTrigger.addEventListener("click", () => fileAudioInput.click());
    fileAudioInput.addEventListener("change", handleFileUpload);

    // Face upload & laptop camera handlers
    if (btnTabCamStart) btnTabCamStart.addEventListener("click", startTabWebcam);
    if (btnTabCamCapture) btnTabCamCapture.addEventListener("click", captureTabWebcamFrame);
    faceDropZone.addEventListener("click", () => fileFaceInput.click());
    fileFaceInput.addEventListener("change", handleFaceSelect);
    btnEvalFace.addEventListener("click", evaluateFaceImage);
    btnResetFace.addEventListener("click", resetFaceUploader);

    // Drag and drop event listeners
    faceDropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        faceDropZone.classList.add("dragover");
    });
    faceDropZone.addEventListener("dragleave", () => {
        faceDropZone.classList.remove("dragover");
    });
    faceDropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        faceDropZone.classList.remove("dragover");
        if (e.dataTransfer.files.length > 0) {
            fileFaceInput.files = e.dataTransfer.files;
            handleFaceSelect();
        }
    });

    // Samples select
    sampleSelect.addEventListener("change", handleSampleSelectChange);
    btnPlaySample.addEventListener("click", playSampleClip);
    btnEvalSample.addEventListener("click", evaluateSampleClip);
    localAudioPlayer.addEventListener("ended", () => {
        btnPlaySample.innerHTML = '<i class="fa-solid fa-play"></i> Play';
    });

    // Manual controls
    btnAgeChild.addEventListener("click", () => setManualAge("Below 18"));
    btnAgeAdult.addEventListener("click", () => setManualAge("18 or Above"));

    // Search input
    appSearchInput.addEventListener("input", filterApps);
}

// --- UI Navigation: Tabs ---
function switchTab(mode) {
    currentVerificationMode = mode;
    
    // Deactivate all
    tabVoice.classList.remove("active");
    tabFace.classList.remove("active");
    tabManual.classList.remove("active");
    contentVoice.classList.remove("active");
    contentFace.classList.remove("active");
    contentManual.classList.remove("active");
    
    if (mode === "voice") {
        tabVoice.classList.add("active");
        contentVoice.classList.add("active");
    } else if (mode === "face") {
        tabFace.classList.add("active");
        contentFace.classList.add("active");
    } else {
        tabManual.classList.add("active");
        contentManual.classList.add("active");
        
        // Update store based on active manual button
        const activeManualAge = btnAgeAdult.classList.contains("active") ? "18 or Above" : "Below 18";
        updateAgeCategory(activeManualAge);
    }
}

function isAdultCategory(ageString) {
    if (!ageString) return false;
    const clean = ageString.trim().toLowerCase();
    if (clean.includes("below") || clean.includes("under") || clean.includes("child") || clean.includes("teen")) {
        return false;
    }
    if (clean.includes("above") || clean.includes("adult") || clean.includes("18+") || clean === "18 or above") {
        return true;
    }
    return false;
}

// --- App Store Rendering & Logic ---
function updateAgeCategory(ageGroup) {
    const isAdult = isAdultCategory(ageGroup);
    currentAgeGroup = isAdult ? "18 or Above" : "Below 18";
    
    // Update top header status badge
    if (currentAgeGroup === "18 or Above") {
        ageStatusBadge.innerHTML = '<span class="pulse-indicator green"></span><span class="badge-label">Age Category: 18+</span>';
    } else {
        ageStatusBadge.innerHTML = '<span class="pulse-indicator yellow"></span><span class="badge-label">Age Category: Below 18</span>';
    }

    renderApps();
}

function renderApps(filterQuery = "") {
    appsContainer.innerHTML = "";
    const query = filterQuery.toLowerCase().trim();

    APPS.forEach((app, index) => {
        if (query && !app.name.toLowerCase().includes(query)) {
            return; // skip if doesn't match search
        }

        const isRestrictedForUser = isProtectionEnabled && (app.isRestricted || customBlockedApps.includes(app.id)) && currentAgeGroup === "Below 18";
        const appCard = document.createElement("div");
        appCard.className = `app-card ${isRestrictedForUser ? 'disabled' : ''}`;
        appCard.setAttribute("data-id", app.id);
        
        // Calculate Grid Position (index is 0 to 24 for a 5x5 grid)
        const row = Math.floor(index / 5) + 1;
        const col = (index % 5) + 1;
        appCard.style.gridRow = row;
        appCard.style.gridColumn = col;

        // Custom styling for icon background
        const textNeedsDark = app.color === "#ffd600" || app.color === "#ffeb3b" || app.color === "#ffffff";
        const iconStyle = `background: ${app.color}; color: ${textNeedsDark ? '#0b0e14' : '#ffffff'}; overflow: hidden;`;

        let badgeHtml = "";
        if (isRestrictedForUser) {
            if (customBlockedApps.includes(app.id) && !app.isRestricted) {
                badgeHtml = `<div class="lock-badge parent-blocked" style="background-color: rgba(255, 152, 0, 0.15); color: var(--secondary); border: 1px solid rgba(255, 152, 0, 0.3);"><i class="fa-solid fa-user-shield"></i> Blocked</div>`;
            } else {
                badgeHtml = `<div class="lock-badge"><i class="fa-solid fa-lock"></i> 18+</div>`;
            }
        } else {
            badgeHtml = `<div class="age-tag">${app.ageLimit}</div>`;
        }

        const imgIconHtml = app.iconUrl ? `<img src="${app.iconUrl}" alt="${app.name}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 16px;" onerror="this.outerHTML='<i class=\\'fa-brands ${app.icon} || fa-solid ${app.icon}\\'></i>'">` : `<i class="fa-brands ${app.icon} || fa-solid ${app.icon}"></i>`;

        appCard.innerHTML = `
            ${badgeHtml}
            <div class="card-icon" style="${iconStyle}">
                ${imgIconHtml}
            </div>
            <h3>${app.name}</h3>
            <span class="app-dev">${app.dev}</span>
            <div class="rating-row">
                <i class="fa-solid fa-star"></i>
                ${app.rating}
                <span>&bull; free</span>
            </div>
            <button class="btn-app-action">
                ${isRestrictedForUser ? '<i class="fa-solid fa-lock"></i> Restricted' : 'Open'}
            </button>
        `;

        // Click interaction
        appCard.addEventListener("click", () => handleAppClick(app, isRestrictedForUser));
        appsContainer.appendChild(appCard);
    });
}

function filterApps(e) {
    renderApps(e.target.value);
}

// --- App Click Handlers (Welcome / Block modals) ---
function handleAppClick(app, isRestricted) {
    modalContainer.classList.remove("hidden");
    
    if (isRestricted) {
        // Show Restricted Modal
        appRestrictedModal.classList.remove("hidden");
        appWelcomeModal.classList.add("hidden");
        document.getElementById("restricted-app-name").innerText = app.name;
    } else {
        // Show Welcome Modal
        appWelcomeModal.classList.remove("hidden");
        appRestrictedModal.classList.add("hidden");
        
        document.getElementById("welcome-app-name").innerText = app.name;
        document.getElementById("welcome-app-dev").innerText = app.dev;
        document.getElementById("welcome-app-rating").innerText = app.rating;
        document.getElementById("welcome-app-age-limit").innerText = app.ageLimit;
        document.getElementById("welcome-brand-text").innerText = app.name;
        
        // Update icon in welcome screen
        const welcomeIconImg = document.getElementById("welcome-app-icon");
        const modalImgIconHtml = app.iconUrl ? `<img src="${app.iconUrl}" alt="${app.name}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 18px;" onerror="this.outerHTML='<i class=\\'fa-brands ${app.icon} || fa-solid ${app.icon}\\'></i>'">` : `<i class="fa-brands ${app.icon} || fa-solid ${app.icon}"></i>`;
        
        welcomeIconImg.outerHTML = `
            <div class="welcome-icon" id="welcome-app-icon" style="background: ${app.color}; display: flex; align-items: center; justify-content: center; font-size: 2.2rem; overflow: hidden; color: ${app.color === '#ffd600' || app.color === '#ffeb3b' || app.color === '#ffffff' ? '#0b0e14' : 'white'}">
                ${modalImgIconHtml}
            </div>
        `;
    }
}

function closeModal() {
    modalContainer.classList.add("hidden");
    appWelcomeModal.classList.add("hidden");
    appRestrictedModal.classList.add("hidden");
}

// --- Manual Age Verification Mode ---
function setManualAge(ageGroup) {
    if (ageGroup === "Below 18") {
        btnAgeChild.classList.add("active");
        btnAgeAdult.classList.remove("active");
    } else {
        btnAgeChild.classList.remove("active");
        btnAgeAdult.classList.add("active");
    }
    
    // Clear prediction outputs to avoid confusion when toggled manually
    inferenceResults.classList.add("hidden");
    
    updateAgeCategory(ageGroup);
}

// --- AI Voice Verification: Recording Logic (WAV Encoder) ---
async function toggleRecording() {
    if (isRecording) {
        stopRecording();
    } else {
        await startRecording();
    }
}

async function startRecording() {
    recordingChunks = [];
    isRecording = true;
    btnRecord.innerHTML = '<i class="fa-solid fa-square"></i> Stop Recording';
    btnRecord.classList.add("recording");
    btnUploadTrigger.disabled = true;

    try {
        mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Audio nodes setup
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        analyserNode = audioContext.createAnalyser();
        analyserNode.fftSize = 256;
        
        micSource = audioContext.createMediaStreamSource(mediaStream);
        
        // Script processor for gathering raw floating-point samples
        scriptProcessor = audioContext.createScriptProcessor(4096, 1, 1);
        
        micSource.connect(analyserNode);
        analyserNode.connect(scriptProcessor);
        scriptProcessor.connect(audioContext.destination);

        scriptProcessor.onaudioprocess = (e) => {
            if (!isRecording) return;
            const channelData = e.inputBuffer.getChannelData(0);
            recordingChunks.push(new Float32Array(channelData));
        };

        // Start visualizer loop
        drawLiveVisualizer();

        // Timer
        recordStartTime = Date.now();
        recordTimer.style.color = "#ff1744";
        recordTimerInterval = setInterval(() => {
            const elapsed = (Date.now() - recordStartTime) / 1000;
            recordTimer.innerText = `${elapsed.toFixed(1)}s`;
            
            // Limit to 5 seconds automatically
            if (elapsed >= RECORD_LIMIT_SEC) {
                stopRecording();
            }
        }, 100);

    } catch (err) {
        console.error("Error accessing microphone:", err);
        alert("Microphone permission denied or microphone not found.");
        resetRecordingState();
    }
}

function stopRecording() {
    if (!isRecording) return;
    isRecording = false;
    resetRecordingState();
    
    // Process recorded buffers and send to backend
    if (recordingChunks.length > 0) {
        processAndSendRecording();
    }
}

function resetRecordingState() {
    btnRecord.innerHTML = '<i class="fa-solid fa-microphone"></i> Start Recording';
    btnRecord.classList.remove("recording");
    btnUploadTrigger.disabled = false;
    recordTimer.style.color = "";

    clearInterval(recordTimerInterval);
    
    if (scriptProcessor) {
        scriptProcessor.disconnect();
        scriptProcessor = null;
    }
    if (micSource) {
        micSource.disconnect();
        micSource = null;
    }
    if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
        mediaStream = null;
    }
    if (audioContext) {
        audioContext.close();
        audioContext = null;
    }
    
    drawIdleVisualizer();
}

// Convert Float32 arrays into a single Float32Array, construct Wav and Upload
function processAndSendRecording() {
    // 1. Flatten all sample chunks
    let totalLength = 0;
    for (let chunk of recordingChunks) {
        totalLength += chunk.length;
    }
    
    let mergedSamples = new Float32Array(totalLength);
    let offset = 0;
    for (let chunk of recordingChunks) {
        mergedSamples.set(chunk, offset);
        offset += chunk.length;
    }
    
    // Create virtual audio buffer (we assume standard user mic sample rate, typically 44.1/48kHz)
    const sampleRate = 44100; // standard fallback
    const offlineCtx = new OfflineAudioContext(1, totalLength, sampleRate);
    const audioBuffer = offlineCtx.createBuffer(1, totalLength, sampleRate);
    audioBuffer.copyToChannel(mergedSamples, 0);
    
    // 2. Encode to WAV
    const wavBlob = bufferToWav(audioBuffer);
    
    // 3. Upload to API
    uploadVoiceFile(wavBlob);
}

function uploadVoiceFile(blobFile) {
    showLoadingState();
    
    const formData = new FormData();
    formData.append("audio", blobFile, "recording.wav");
    
    fetch("/api/predict", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        handlePredictionSuccess(data, "AI Voice Verification");
    })
    .catch(err => {
        console.error(err);
        alert("Connection to classification backend failed.");
        hideLoadingState();
    });
}

// --- Audio Visualizer Drawing ---
function drawIdleVisualizer() {
    canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
    canvasCtx.strokeStyle = "rgba(148, 163, 184, 0.2)";
    canvasCtx.lineWidth = 2;
    canvasCtx.beginPath();
    canvasCtx.moveTo(0, canvas.height / 2);
    canvasCtx.lineTo(canvas.width, canvas.height / 2);
    canvasCtx.stroke();
}

function drawLiveVisualizer() {
    if (!isRecording || !analyserNode) return;
    
    requestAnimationFrame(drawLiveVisualizer);
    
    const bufferLength = analyserNode.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    analyserNode.getByteTimeDomainData(dataArray);
    
    canvasCtx.fillStyle = "rgba(11, 14, 20, 0.4)";
    canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
    
    canvasCtx.lineWidth = 3;
    canvasCtx.strokeStyle = "var(--danger)";
    canvasCtx.beginPath();
    
    const sliceWidth = canvas.width * 1.0 / bufferLength;
    let x = 0;
    
    for (let i = 0; i < bufferLength; i++) {
        const v = dataArray[i] / 128.0;
        const y = v * canvas.height / 2;
        
        if (i === 0) {
            canvasCtx.moveTo(x, y);
        } else {
            canvasCtx.lineTo(x, y);
        }
        
        x += sliceWidth;
    }
    
    canvasCtx.lineTo(canvas.width, canvas.height / 2);
    canvasCtx.stroke();
}

// --- WAV Audio Encoder Utility ---
function bufferToWav(buffer) {
    let numOfChan = buffer.numberOfChannels,
        length = buffer.length * numOfChan * 2 + 44,
        bufferArr = new ArrayBuffer(length),
        view = new DataView(bufferArr),
        channels = [], i, sample,
        offset = 0,
        pos = 0;

    // write HEADERS
    setUint32(0x46464952); // "RIFF"
    setUint32(length - 8); // file length - 8
    setUint32(0x45564157); // "WAVE"
    setUint32(0x20746d66); // "fmt " chunk
    setUint32(16);         // length = 16
    setUint16(1);          // PCM = 1
    setUint16(numOfChan);
    setUint32(buffer.sampleRate);
    setUint32(buffer.sampleRate * 2 * numOfChan); // byte rate
    setUint16(numOfChan * 2); // block align
    setUint16(16);         // bits per sample = 16
    setUint32(0x61746164); // "data" chunk
    setUint32(length - pos - 4); // chunk length

    // write interleaved data
    for(i=0; i<buffer.numberOfChannels; i++)
        channels.push(buffer.getChannelData(i));

    while(pos < length) {
        for(i=0; i<numOfChan; i++) {             // interleave channels
            sample = Math.max(-1, Math.min(1, channels[i][offset])); // clamp
            sample = (sample < 0 ? sample * 0x8000 : sample * 0x7FFF); // scale to 16-bit signed int
            view.setInt16(pos, sample, true);          // write 16-bit sample
            pos += 2;
        }
        offset++;
    }

    return new Blob([bufferArr], {type: "audio/wav"});

    function setUint16(data) {
        view.setUint16(pos, data, true);
        pos += 2;
    }

    function setUint32(data) {
        view.setUint32(pos, data, true);
        pos += 4;
    }
}

// --- Upload File Logic ---
function handleFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    
    showLoadingState();
    
    const formData = new FormData();
    formData.append("audio", file);
    
    fetch("/api/predict", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        handlePredictionSuccess(data, "File Upload Verification");
        fileAudioInput.value = ""; // reset input
    })
    .catch(err => {
        console.error(err);
        alert("Classification server returned an error.");
        hideLoadingState();
        fileAudioInput.value = "";
    });
}

// --- Sample Audio Playback & Integration ---
function loadSampleClips() {
    fetch("/api/samples")
    .then(res => res.json())
    .then(samples => {
        samples.forEach(s => {
            const opt = document.createElement("option");
            opt.value = s.filename;
            opt.innerText = s.label;
            sampleSelect.appendChild(opt);
        });
    })
    .catch(err => console.error("Error loading demo samples list:", err));
}

function handleSampleSelectChange() {
    const selected = sampleSelect.value;
    if (selected) {
        btnPlaySample.disabled = false;
        btnEvalSample.disabled = false;
        localAudioPlayer.src = `/api/samples/${selected}`;
    } else {
        btnPlaySample.disabled = true;
        btnEvalSample.disabled = true;
    }
}

function playSampleClip() {
    if (localAudioPlayer.paused) {
        localAudioPlayer.play();
        btnPlaySample.innerHTML = '<i class="fa-solid fa-pause"></i> Pause';
    } else {
        localAudioPlayer.pause();
        btnPlaySample.innerHTML = '<i class="fa-solid fa-play"></i> Play';
    }
}

function evaluateSampleClip() {
    const selected = sampleSelect.value;
    if (!selected) return;
    
    showLoadingState();
    
    fetch(`/api/predict-sample/${selected}`, {
        method: "POST"
    })
    .then(res => res.json())
    .then(data => {
        handlePredictionSuccess(data, `Sample: ${selected}`);
    })
    .catch(err => {
        console.error(err);
        alert("Sample classification failed.");
        hideLoadingState();
    });
}

// --- Inference State Management UI ---
function showLoadingState() {
    inferenceResults.classList.remove("hidden");
    resBadgeType.innerText = "Analyzing...";
    resClass.innerText = "Processing...";
    resClass.style.color = "var(--text-secondary)";
    resProb.innerText = "-";
    resConfidence.innerText = "-";
    resProgressIndicator.style.width = "50%";
    
    const labelElem = document.querySelector(".res-label");
    if (labelElem) {
        labelElem.innerText = "Detected Class:";
    }
}

function hideLoadingState() {
    inferenceResults.classList.add("hidden");
}

function handlePredictionSuccess(data, modeName) {
    if (!data.success) {
        alert("Backend failed to classify audio: " + data.error);
        hideLoadingState();
        return;
    }
    
    // Display results in left card panel
    inferenceResults.classList.remove("hidden");
    resBadgeType.innerText = modeName;
    resClass.innerText = data.predicted_class;
    
    if (isAdultCategory(data.predicted_class)) {
        resClass.style.color = "var(--primary)";
    } else {
        resClass.style.color = "var(--accent)";
    }
    
    resProb.innerText = data.probability.toFixed(4);
    resConfidence.innerText = `${(data.confidence * 100).toFixed(1)}%`;
    
    // Update progress bar indicator
    resProgressIndicator.style.width = `${(data.probability * 100).toFixed(0)}%`;
    
    // Propagate update to active layout state
    updateAgeCategory(data.predicted_class);
}

// --- AI Face Verification Handlers ---
let selectedFaceFile = null;

function handleFaceSelect() {
    const file = fileFaceInput.files[0];
    if (!file) return;

    selectedFaceFile = file;

    const reader = new FileReader();
    reader.onload = (e) => {
        uploadedImagePreview.src = e.target.result;
        previewWrapper.classList.remove("hidden");
        
        faceCropPreviewBox.classList.add("hidden");
        croppedFacePreview.src = "";

        btnEvalFace.disabled = false;
        btnResetFace.classList.remove("hidden");
    };
    reader.readAsDataURL(file);
}

function resetFaceUploader() {
    stopTabWebcamStream();
    selectedFaceFile = null;
    fileFaceInput.value = "";
    uploadedImagePreview.src = "";
    croppedFacePreview.src = "";
    previewWrapper.classList.add("hidden");
    faceCropPreviewBox.classList.add("hidden");
    btnEvalFace.disabled = true;
    btnResetFace.classList.add("hidden");
    hideLoadingState();
}

async function startTabWebcam() {
    try {
        if (!faceWebcamCard) return;
        tabWebcamStatus.innerText = "Requesting laptop camera access...";
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { width: { ideal: 320 }, height: { ideal: 320 } }
        });
        tabWebcamMediaStream = stream;
        tabWebcamStream.srcObject = stream;
        tabWebcamStream.style.display = "block";
        faceWebcamCard.classList.remove("hidden");
        
        btnTabCamStart.classList.add("hidden");
        btnTabCamCapture.classList.remove("hidden");
        btnResetFace.classList.remove("hidden");

        const scanner = faceWebcamCard.querySelector(".scanner-circle");
        if (scanner) scanner.classList.add("active");

        tabWebcamStatus.innerText = "Align your face in the circle and click Capture Face.";
    } catch (err) {
        console.error("Laptop camera access failed:", err);
        if (tabWebcamStatus) tabWebcamStatus.innerText = "Camera access denied or laptop camera not found.";
        alert("Laptop camera permission denied or camera not found.");
    }
}

function stopTabWebcamStream() {
    if (tabWebcamMediaStream) {
        tabWebcamMediaStream.getTracks().forEach(track => track.stop());
        tabWebcamMediaStream = null;
    }
    if (tabWebcamStream) {
        tabWebcamStream.srcObject = null;
        tabWebcamStream.style.display = "none";
    }
    if (faceWebcamCard) {
        faceWebcamCard.classList.add("hidden");
        const scanner = faceWebcamCard.querySelector(".scanner-circle");
        if (scanner) scanner.classList.remove("active");
    }
    if (btnTabCamStart) btnTabCamStart.classList.remove("hidden");
    if (btnTabCamCapture) btnTabCamCapture.classList.add("hidden");
}

function captureTabWebcamFrame() {
    if (!tabWebcamMediaStream) return;
    try {
        tabWebcamStatus.innerText = "Capturing frame from laptop camera...";
        const context = tabCaptureCanvas.getContext("2d");
        tabCaptureCanvas.width = 224;
        tabCaptureCanvas.height = 224;
        
        context.drawImage(tabWebcamStream, 0, 0, tabCaptureCanvas.width, tabCaptureCanvas.height);
        
        // Show captured image preview
        const dataUrl = tabCaptureCanvas.toDataURL("image/jpeg");
        uploadedImagePreview.src = dataUrl;
        previewWrapper.classList.remove("hidden");

        // Stop live webcam feed
        stopTabWebcamStream();

        // Convert canvas to Blob & store as selectedFaceFile
        tabCaptureCanvas.toBlob((blob) => {
            selectedFaceFile = new File([blob], "laptop_cam_capture.jpg", { type: "image/jpeg" });
            btnEvalFace.disabled = false;
            // Automatically classify captured face
            evaluateFaceImage();
        }, "image/jpeg", 0.95);

    } catch (err) {
        console.error("Frame capture error:", err);
        tabWebcamStatus.innerText = "Frame capture failed.";
        stopTabWebcamStream();
    }
}

function evaluateFaceImage() {
    if (!selectedFaceFile) return;

    showLoadingState();
    resClass.innerText = "Processing face...";

    const formData = new FormData();
    formData.append("image", selectedFaceFile);

    fetch("/api/predict-face", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        hideLoadingState();
        inferenceResults.classList.remove("hidden");
        resBadgeType.innerText = "AI Face Verification";

        if (!data.success || data.face_detected === false || (data.error && data.error.includes("Face is not recorder"))) {
            resClass.innerText = "Face is not recorder";
            resClass.style.color = "var(--danger)";
            resProb.innerText = "Camera Blocked / No Face";
            resConfidence.innerText = "0.0%";
            resProgressIndicator.style.width = "0%";
            faceCropPreviewBox.classList.add("hidden");

            // Inform user and automatically switch to Voice Age Prediction
            setTimeout(() => {
                alert("Face is not recorder. Switching to Voice Age Prediction so age can be predicted based on voice.");
                switchTab("voice");
            }, 600);
            return;
        }

        resClass.innerText = data.overall_class;

        if (isAdultCategory(data.overall_class)) {
            resClass.style.color = "var(--primary)";
        } else {
            resClass.style.color = "var(--accent)";
        }

        const mainPred = data.predictions ? data.predictions[0] : {};
        resProb.innerText = mainPred.predicted_bin || "-"; 
        
        const labelElem = document.querySelector(".res-label");
        if (labelElem) {
            labelElem.innerText = "Predicted Bin:";
        }
        
        resConfidence.innerText = mainPred.confidence ? `${(mainPred.confidence * 100).toFixed(1)}%` : "-";
        resProgressIndicator.style.width = mainPred.confidence ? `${(mainPred.confidence * 100).toFixed(0)}%` : "50%";

        if (mainPred.crop_relative_path) {
            const cropUrl = `/${mainPred.crop_relative_path}`;
            croppedFacePreview.src = `${cropUrl}?t=${Date.now()}`;
            faceCropPreviewBox.classList.remove("hidden");
        }

        updateAgeCategory(data.overall_class);
    })
    .catch(err => {
        console.error(err);
        alert("Face classification request failed.");
        hideLoadingState();
    });
}

// --- Multi-Modal Age Verification Wizard Logic ---
let wizardFaceResult = null;
let wizardVoiceResult = null;
let wizardWebcamStream = null;
let wizardIsRecording = false;

// Audio context & recording variables for wizard
let wizardAudioContext = null;
let wizardAnalyserNode = null;
let wizardMicSource = null;
let wizardScriptProcessor = null;
let wizardRecordingChunks = [];
let wizardRecordStartTime = 0;
let wizardRecordTimerInterval = null;

function initWizard() {
    // Face step events
    btnWizardScan.addEventListener("click", toggleWizardWebcam);
    btnWizardUploadFaceTrigger.addEventListener("click", () => wizardFileFaceInput.click());
    wizardFileFaceInput.addEventListener("change", handleWizardFaceUpload);

    // Voice step events
    btnWizardRecord.addEventListener("click", toggleWizardVoiceRecording);
    btnWizardUploadVoiceTrigger.addEventListener("click", () => wizardFileAudioInput.click());
    wizardFileAudioInput.addEventListener("change", handleWizardVoiceUpload);

    // Enter store
    btnWizardEnter.addEventListener("click", enterPlayStoreFromWizard);

    // Visualizer flatline
    drawWizardVoiceIdle();
}

// STEP 1: Face Scan Functions
async function toggleWizardWebcam() {
    if (!wizardWebcamStream) {
        // Start live stream
        try {
            wizardFaceStatus.innerText = "Requesting webcam access...";
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { width: { ideal: 320 }, height: { ideal: 320 } }
            });
            wizardWebcamStream = stream;
            webcamStream.srcObject = stream;
            webcamStream.style.display = "block";
            scannerPlaceholder.style.display = "none";
            
            const scanner = document.querySelector(".scanner-circle");
            if (scanner) scanner.classList.add("active");

            btnWizardScan.innerHTML = '<i class="fa-solid fa-circle-dot"></i> Capture Face';
            wizardFaceStatus.innerText = "Align your face in the circle and click Capture Face.";
        } catch (err) {
            console.error("Camera access failed:", err);
            wizardFaceStatus.innerText = "Webcam access denied. Please upload a photo instead.";
            alert("Webcam permission denied or webcam not found.");
        }
    } else {
        // Capture frame & stop stream
        try {
            wizardFaceStatus.innerText = "Analyzing captured frame...";
            const context = captureCanvas.getContext("2d");
            captureCanvas.width = 224;
            captureCanvas.height = 224;
            
            // Draw video crop to square canvas
            context.drawImage(webcamStream, 0, 0, captureCanvas.width, captureCanvas.height);
            
            // Stop webcam tracks
            stopWebcamStream();

            // Convert canvas to Blob & upload
            captureCanvas.toBlob((blob) => {
                uploadWizardFaceFile(blob);
            }, "image/jpeg", 0.95);

        } catch (err) {
            console.error("Frame capture error:", err);
            wizardFaceStatus.innerText = "Frame capture failed.";
            resetWizardWebcamUI();
        }
    }
}

function stopWebcamStream() {
    if (wizardWebcamStream) {
        wizardWebcamStream.getTracks().forEach(track => track.stop());
        wizardWebcamStream = null;
    }
    webcamStream.srcObject = null;
    webcamStream.style.display = "none";
    scannerPlaceholder.style.display = "block";
    
    const scanner = document.querySelector(".scanner-circle");
    if (scanner) {
        scanner.classList.remove("active");
    }
}

function resetWizardWebcamUI() {
    stopWebcamStream();
    btnWizardScan.innerHTML = '<i class="fa-solid fa-camera"></i> Start Live Scan';
}

function handleWizardFaceUpload() {
    const file = wizardFileFaceInput.files[0];
    if (!file) return;
    uploadWizardFaceFile(file);
}

function uploadWizardFaceFile(fileBlob) {
    wizardFaceStatus.innerText = "Analyzing Face Image...";
    btnWizardScan.disabled = true;
    btnWizardUploadFaceTrigger.disabled = true;

    const formData = new FormData();
    formData.append("image", fileBlob, "face.jpg");

    fetch("/api/predict-face", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        btnWizardScan.disabled = false;
        btnWizardUploadFaceTrigger.disabled = false;
        
        const scanner = document.querySelector(".scanner-circle");
        if (scanner) scanner.classList.add("completed");

        if (!data.success || data.face_detected === false || (data.error && data.error.includes("Face is not recorder"))) {
            wizardFaceResult = {
                face_detected: false,
                overall_class: "Face is not recorder",
                predicted_bin: "Camera Blocked",
                confidence: 0,
                status: "Face is not recorder"
            };

            wizardFaceStatus.innerHTML = '<span style="color: var(--danger); font-weight: 600;">Face is not recorder</span>. Proceeding to Voice Age Prediction...';
            
            // Progress step tracker
            dotStep1.classList.add("completed");
            document.querySelectorAll(".step-line")[0].classList.add("completed");

            // Transition automatically to Step 2 (Voice Age Scan) after 1.5 seconds
            setTimeout(() => {
                wizardStep1.classList.remove("active");
                wizardStep2.classList.add("active");
                dotStep2.classList.add("active");
            }, 1500);
            return;
        }

        const mainPred = data.predictions ? data.predictions[0] : {};
        wizardFaceResult = {
            face_detected: true,
            overall_class: data.overall_class,
            predicted_bin: mainPred.predicted_bin,
            confidence: mainPred.confidence
        };

        wizardFaceStatus.innerText = `Scan Successful! Category: ${data.overall_class}`;
        
        // Progress step tracker
        dotStep1.classList.add("completed");
        document.querySelectorAll(".step-line")[0].classList.add("completed");

        // Transition to Step 2 after 1.5 seconds
        setTimeout(() => {
            wizardStep1.classList.remove("active");
            wizardStep2.classList.add("active");
            dotStep2.classList.add("active");
        }, 1500);
    })
    .catch(err => {
        console.error(err);
        wizardFaceStatus.innerText = "Face prediction API request failed.";
        btnWizardScan.disabled = false;
        btnWizardUploadFaceTrigger.disabled = false;
        resetWizardWebcamUI();
    });
}

// STEP 2: Voice Verification Functions
async function toggleWizardVoiceRecording() {
    if (wizardIsRecording) {
        stopWizardVoiceRecording(false);
    } else {
        await startWizardVoiceRecording();
    }
}

async function startWizardVoiceRecording() {
    wizardRecordingChunks = [];
    wizardIsRecording = true;
    btnWizardRecord.innerHTML = '<i class="fa-solid fa-square"></i> Stop Recording';
    btnWizardRecord.classList.add("recording");
    btnWizardUploadVoiceTrigger.disabled = true;
    wizardVoiceStatus.innerText = "Recording voice... please speak.";

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        wizardAudioContext = new (window.AudioContext || window.webkitAudioContext)();
        wizardAnalyserNode = wizardAudioContext.createAnalyser();
        wizardAnalyserNode.fftSize = 256;
        
        wizardMicSource = wizardAudioContext.createMediaStreamSource(stream);
        wizardScriptProcessor = wizardAudioContext.createScriptProcessor(4096, 1, 1);
        
        wizardMicSource.connect(wizardAnalyserNode);
        wizardAnalyserNode.connect(wizardScriptProcessor);
        wizardScriptProcessor.connect(wizardAudioContext.destination);

        wizardScriptProcessor.onaudioprocess = (e) => {
            if (!wizardIsRecording) return;
            const channelData = e.inputBuffer.getChannelData(0);
            wizardRecordingChunks.push(new Float32Array(channelData));
        };

        drawWizardVoiceLive();

        // 5-second countdown & progress ring animation
        wizardRecordStartTime = Date.now();
        wizardVoiceProgressBar.style.strokeDashoffset = "0";
        
        wizardRecordTimerInterval = setInterval(() => {
            const elapsed = (Date.now() - wizardRecordStartTime) / 1000;
            const remaining = Math.max(0, RECORD_LIMIT_SEC - elapsed);
            wizardVoiceTimer.innerText = `${remaining.toFixed(1)}s`;
            
            const offset = (elapsed / RECORD_LIMIT_SEC) * 282.7;
            wizardVoiceProgressBar.style.strokeDashoffset = offset.toFixed(1);

            if (elapsed >= RECORD_LIMIT_SEC) {
                stopWizardVoiceRecording(true);
            }
        }, 50);

    } catch (err) {
        console.error("Microphone access failed:", err);
        wizardVoiceStatus.innerText = "Microphone access denied. Please upload an audio file.";
        resetWizardVoiceUI();
    }
}

function stopWizardVoiceRecording(shouldUpload) {
    if (!wizardIsRecording) return;
    wizardIsRecording = false;
    
    clearInterval(wizardRecordTimerInterval);
    btnWizardRecord.innerHTML = '<i class="fa-solid fa-microphone"></i> Start Voice Record';
    btnWizardRecord.classList.remove("recording");
    btnWizardUploadVoiceTrigger.disabled = false;

    if (wizardScriptProcessor) {
        wizardScriptProcessor.disconnect();
        wizardScriptProcessor = null;
    }
    if (wizardMicSource) {
        wizardMicSource.disconnect();
        wizardMicSource = null;
    }
    if (wizardAudioContext) {
        wizardAudioContext.close();
        wizardAudioContext = null;
    }

    drawWizardVoiceIdle();

    if (shouldUpload && wizardRecordingChunks.length > 0) {
        processAndSendWizardVoice();
    }
}

function resetWizardVoiceUI() {
    stopWizardVoiceRecording(false);
    wizardVoiceTimer.innerText = "5.0s";
    wizardVoiceProgressBar.style.strokeDashoffset = "0";
}

function processAndSendWizardVoice() {
    wizardVoiceStatus.innerText = "Encoding WAV...";
    let totalLength = 0;
    for (let chunk of wizardRecordingChunks) {
        totalLength += chunk.length;
    }
    
    let mergedSamples = new Float32Array(totalLength);
    let offset = 0;
    for (let chunk of wizardRecordingChunks) {
        mergedSamples.set(chunk, offset);
        offset += chunk.length;
    }
    
    const sampleRate = 44100;
    const offlineCtx = new OfflineAudioContext(1, totalLength, sampleRate);
    const audioBuffer = offlineCtx.createBuffer(1, totalLength, sampleRate);
    audioBuffer.copyToChannel(mergedSamples, 0);
    
    const wavBlob = bufferToWav(audioBuffer);
    uploadWizardVoiceFile(wavBlob);
}

function handleWizardVoiceUpload() {
    const file = wizardFileAudioInput.files[0];
    if (!file) return;
    uploadWizardVoiceFile(file);
}

function uploadWizardVoiceFile(fileBlob) {
    wizardVoiceStatus.innerText = "Analyzing voice clip...";
    btnWizardRecord.disabled = true;
    btnWizardUploadVoiceTrigger.disabled = true;

    const formData = new FormData();
    formData.append("audio", fileBlob, "recording.wav");

    fetch("/api/predict", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        btnWizardRecord.disabled = false;
        btnWizardUploadVoiceTrigger.disabled = false;

        if (!data.success) {
            wizardVoiceStatus.innerText = "Voice classification failed: " + data.error;
            resetWizardVoiceUI();
            return;
        }

        wizardVoiceResult = {
            predicted_class: data.predicted_class,
            probability: data.probability,
            confidence: data.confidence
        };

        wizardVoiceStatus.innerText = `Voice Verified! Category: ${data.predicted_class}`;
        
        dotStep2.classList.add("completed");
        document.querySelectorAll(".step-line")[1].classList.add("completed");

        // Transition to Step 3 after 1.5 seconds
        setTimeout(() => {
            wizardStep2.classList.remove("active");
            wizardStep3.classList.add("active");
            dotStep3.classList.add("active");
            evaluateConsolidatedResults();
        }, 1500);
    })
    .catch(err => {
        console.error(err);
        wizardVoiceStatus.innerText = "Voice prediction API request failed.";
        btnWizardRecord.disabled = false;
        btnWizardUploadVoiceTrigger.disabled = false;
        resetWizardVoiceUI();
    });
}

function drawWizardVoiceIdle() {
    wizardVoiceVisualizerCtx.clearRect(0, 0, wizardVoiceVisualizer.width, wizardVoiceVisualizer.height);
    wizardVoiceVisualizerCtx.strokeStyle = "rgba(148, 163, 184, 0.2)";
    wizardVoiceVisualizerCtx.lineWidth = 2;
    wizardVoiceVisualizerCtx.beginPath();
    wizardVoiceVisualizerCtx.moveTo(0, wizardVoiceVisualizer.height / 2);
    wizardVoiceVisualizerCtx.lineTo(wizardVoiceVisualizer.width, wizardVoiceVisualizer.height / 2);
    wizardVoiceVisualizerCtx.stroke();
}

function drawWizardVoiceLive() {
    if (!wizardIsRecording || !wizardAnalyserNode) return;
    requestAnimationFrame(drawWizardVoiceLive);
    
    const bufferLength = wizardAnalyserNode.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    wizardAnalyserNode.getByteTimeDomainData(dataArray);
    
    wizardVoiceVisualizerCtx.fillStyle = "rgba(11, 14, 20, 0.4)";
    wizardVoiceVisualizerCtx.fillRect(0, 0, wizardVoiceVisualizer.width, wizardVoiceVisualizer.height);
    
    wizardVoiceVisualizerCtx.lineWidth = 3;
    wizardVoiceVisualizerCtx.strokeStyle = "var(--danger)";
    wizardVoiceVisualizerCtx.beginPath();
    
    const sliceWidth = wizardVoiceVisualizer.width * 1.0 / bufferLength;
    let x = 0;
    
    for (let i = 0; i < bufferLength; i++) {
        const v = dataArray[i] / 128.0;
        const y = v * wizardVoiceVisualizer.height / 2;
        
        if (i === 0) {
            wizardVoiceVisualizerCtx.moveTo(x, y);
        } else {
            wizardVoiceVisualizerCtx.lineTo(x, y);
        }
        x += sliceWidth;
    }
    
    wizardVoiceVisualizerCtx.lineTo(wizardVoiceVisualizer.width, wizardVoiceVisualizer.height / 2);
    wizardVoiceVisualizerCtx.stroke();
}

// STEP 3: Consolidated Evaluation Functions
function evaluateConsolidatedResults() {
    try {
        if (!wizardFaceResult || !wizardVoiceResult) {
            console.warn("evaluateConsolidatedResults: results not fully populated yet.");
            return;
        }

        const fClass = wizardFaceResult.overall_class || "Unknown";
        const vClass = wizardVoiceResult.predicted_class || "Unknown";

        const fClassClean = fClass.trim().toLowerCase();
        const vClassClean = vClass.trim().toLowerCase();

        const fIsAdult = isAdultCategory(fClass);
        const vIsAdult = isAdultCategory(vClass);

        const fConf = wizardFaceResult.confidence !== undefined ? (wizardFaceResult.confidence * 100).toFixed(1) : "0.0";
        const vConf = wizardVoiceResult.confidence !== undefined ? (wizardVoiceResult.confidence * 100).toFixed(1) : "0.0";
        const vProb = wizardVoiceResult.probability !== undefined ? wizardVoiceResult.probability.toFixed(4) : "0.0000";

        // Display side-by-side card results
        if (wizardResFacePill) wizardResFacePill.innerText = fClass;
        if (wizardResFaceBin) wizardResFaceBin.innerText = `Bin: ${wizardFaceResult.predicted_bin || '-'}`;
        if (wizardResFaceConf) wizardResFaceConf.innerText = wizardFaceResult.face_detected === false ? "N/A" : `Conf: ${fConf}%`;

        if (wizardResVoicePill) wizardResVoicePill.innerText = vClass;
        if (wizardResVoiceBin) wizardResVoiceBin.innerText = `Prob: ${vProb}`;
        if (wizardResVoiceConf) wizardResVoiceConf.innerText = `Conf: ${vConf}%`;

        const cardFace = document.getElementById("wizard-card-face");
        const cardVoice = document.getElementById("wizard-card-voice");

        // Handle camera blocked / Face is not recorder
        if (wizardFaceResult.face_detected === false || fClass === "Face is not recorder") {
            if (cardFace) {
                cardFace.classList.add("conflict");
                cardFace.classList.remove("match");
            }
            if (cardVoice) {
                cardVoice.classList.add("match");
                cardVoice.classList.remove("conflict");
            }

            if (vIsAdult) {
                if (wizardVerdictBox) wizardVerdictBox.className = "verdict-display-box unlock";
                if (wizardVerdictTitle) wizardVerdictTitle.innerText = "Verification Verdict: UNLOCKED (Voice-Based)";
                if (wizardVerdictDesc) wizardVerdictDesc.innerText = "Face is not recorder. Age predicted based on voice classification as 18 or older. VoiceVision access fully unlocked.";
                currentAgeGroup = "18 or Above";
            } else {
                if (wizardVerdictBox) wizardVerdictBox.className = "verdict-display-box restrict";
                if (wizardVerdictTitle) wizardVerdictTitle.innerText = "Verification Verdict: RESTRICTED (Voice-Based)";
                if (wizardVerdictDesc) wizardVerdictDesc.innerText = "Face is not recorder. Age predicted based on voice classification as under 18. Store limited to child-friendly content.";
                currentAgeGroup = "Below 18";
            }
        } else if (fIsAdult === vIsAdult) {
            if (cardFace) {
                cardFace.classList.add("match");
                cardFace.classList.remove("conflict");
            }
            if (cardVoice) {
                cardVoice.classList.add("match");
                cardVoice.classList.remove("conflict");
            }

            if (fIsAdult) {
                if (wizardVerdictBox) wizardVerdictBox.className = "verdict-display-box unlock";
                if (wizardVerdictTitle) wizardVerdictTitle.innerText = "Verification Verdict: UNLOCKED";
                if (wizardVerdictDesc) wizardVerdictDesc.innerText = "Both face and voice classification models agree you are 18 or older. VoiceVision access fully unlocked.";
                currentAgeGroup = "18 or Above";
            } else {
                if (wizardVerdictBox) wizardVerdictBox.className = "verdict-display-box restrict";
                if (wizardVerdictTitle) wizardVerdictTitle.innerText = "Verification Verdict: RESTRICTED";
                if (wizardVerdictDesc) wizardVerdictDesc.innerText = "Both face and voice classification models agree you are under 18. Store limited to child-friendly content for safety.";
                currentAgeGroup = "Below 18";
            }
        } else {
            if (cardFace) {
                cardFace.classList.add("conflict");
                cardFace.classList.remove("match");
            }
            if (cardVoice) {
                cardVoice.classList.add("conflict");
                cardVoice.classList.remove("match");
            }

            if (wizardVerdictBox) wizardVerdictBox.className = "verdict-display-box conflict";
            if (wizardVerdictTitle) wizardVerdictTitle.innerText = "Verification Verdict: RESTRICTED (CONFLICT)";
            if (wizardVerdictDesc) wizardVerdictDesc.innerText = `Verification conflict! Face Model: ${fClass}, Voice Model: ${vClass}. For safety and parental control compliance, access is restricted.`;
            currentAgeGroup = "Below 18";
        }
    } catch (e) {
        console.error("Error in evaluateConsolidatedResults:", e);
    } finally {
        if (btnWizardEnter) {
            btnWizardEnter.disabled = false;
        }
        if (dotStep3) {
            dotStep3.classList.add("completed");
        }
    }
}

function enterPlayStoreFromWizard() {
    // Stop all audio/video streams just in case
    stopWebcamStream();
    
    // Set age status globally in store app layout
    updateAgeCategory(currentAgeGroup);
    syncPortalState();

    // Hide the wizard modal and overlay
    wizardContainer.classList.add("hidden");
}

// --- NLP Voice Assistant Controller Logic ---
let assistantIsRecording = false;
let assistantRecordingChunks = [];
let assistantAudioContext = null;
let assistantAnalyserNode = null;
let assistantMicSource = null;
let assistantScriptProcessor = null;
let assistantRecordStartTime = 0;
let assistantRecordTimerInterval = null;

function initAssistant() {
    // Open/Close Drawer Toggle
    btnAssistantToggle.addEventListener("click", () => {
        assistantDrawer.classList.toggle("hidden");
        if (!assistantDrawer.classList.contains("hidden")) {
            drawAssistantVoiceIdle();
        }
    });

    btnAssistantClose.addEventListener("click", () => {
        assistantDrawer.classList.add("hidden");
        stopAssistantRecording(false);
    });

    // Recording Controls
    btnAssistantRecord.addEventListener("click", toggleAssistantRecording);
    btnAssistantUploadTrigger.addEventListener("click", () => assistantFileInput.click());
    assistantFileInput.addEventListener("change", handleAssistantFileUpload);

    // Initial Visualizer Flatline
    drawAssistantVoiceIdle();

    // Listen to spacebar to trigger voice command
    document.addEventListener("keydown", (e) => {
        if (e.code === "Space" && !assistantDrawer.classList.contains("hidden")) {
            if (document.activeElement.tagName !== "INPUT" && document.activeElement.tagName !== "TEXTAREA") {
                e.preventDefault();
                toggleAssistantRecording();
            }
        }
    });
}

async function toggleAssistantRecording() {
    if (assistantIsRecording) {
        stopAssistantRecording(true);
    } else {
        await startAssistantRecording();
    }
}

async function startAssistantRecording() {
    assistantRecordingChunks = [];
    assistantIsRecording = true;
    btnAssistantRecord.innerHTML = '<i class="fa-solid fa-square"></i> Stop Command';
    btnAssistantRecord.classList.add("recording");
    btnAssistantUploadTrigger.disabled = true;
    assistantHint.innerText = "Recording... speak now, then click Stop or press Spacebar.";
    
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        assistantAudioContext = new (window.AudioContext || window.webkitAudioContext)();
        assistantAnalyserNode = assistantAudioContext.createAnalyser();
        assistantAnalyserNode.fftSize = 256;
        
        assistantMicSource = assistantAudioContext.createMediaStreamSource(stream);
        assistantScriptProcessor = assistantAudioContext.createScriptProcessor(4096, 1, 1);
        
        assistantMicSource.connect(assistantAnalyserNode);
        assistantAnalyserNode.connect(assistantScriptProcessor);
        assistantScriptProcessor.connect(assistantAudioContext.destination);

        assistantScriptProcessor.onaudioprocess = (e) => {
            if (!assistantIsRecording) return;
            const channelData = e.inputBuffer.getChannelData(0);
            assistantRecordingChunks.push(new Float32Array(channelData));
        };

        drawAssistantVoiceLive();

        // 5-second max limit countdown
        assistantRecordStartTime = Date.now();
        assistantRecordTimerInterval = setInterval(() => {
            const elapsed = (Date.now() - assistantRecordStartTime) / 1000;
            assistantTimer.innerText = `${elapsed.toFixed(1)}s`;
            
            if (elapsed >= RECORD_LIMIT_SEC) {
                stopAssistantRecording(true);
            }
        }, 100);

    } catch (err) {
        console.error("Assistant microphone access error:", err);
        assistantHint.innerText = "Microphone access denied. Try uploading a WAV file.";
        resetAssistantRecordingUI();
    }
}

function stopAssistantRecording(shouldSubmit) {
    if (!assistantIsRecording) return;
    assistantIsRecording = false;
    
    clearInterval(assistantRecordTimerInterval);
    btnAssistantRecord.innerHTML = '<i class="fa-solid fa-microphone"></i> Speak Command';
    btnAssistantRecord.classList.remove("recording");
    btnAssistantUploadTrigger.disabled = false;
    assistantTimer.innerText = "0.0s";

    if (assistantScriptProcessor) {
        assistantScriptProcessor.disconnect();
        assistantScriptProcessor = null;
    }
    if (assistantMicSource) {
        assistantMicSource.disconnect();
        assistantMicSource = null;
    }
    if (assistantAudioContext) {
        assistantAudioContext.close();
        assistantAudioContext = null;
    }

    drawAssistantVoiceIdle();

    if (shouldSubmit && assistantRecordingChunks.length > 0) {
        processAndSendAssistantAudio();
    }
}

function resetAssistantRecordingUI() {
    stopAssistantRecording(false);
    assistantTimer.innerText = "0.0s";
}

function processAndSendAssistantAudio() {
    assistantHint.innerText = "Encoding WAV...";
    let totalLength = 0;
    for (let chunk of assistantRecordingChunks) {
        totalLength += chunk.length;
    }
    
    let mergedSamples = new Float32Array(totalLength);
    let offset = 0;
    for (let chunk of assistantRecordingChunks) {
        mergedSamples.set(chunk, offset);
        offset += chunk.length;
    }
    
    const sampleRate = 44100;
    const offlineCtx = new OfflineAudioContext(1, totalLength, sampleRate);
    const audioBuffer = offlineCtx.createBuffer(1, totalLength, sampleRate);
    audioBuffer.copyToChannel(mergedSamples, 0);
    
    const wavBlob = bufferToWav(audioBuffer);
    uploadAssistantAudio(wavBlob);
}

function handleAssistantFileUpload() {
    const file = assistantFileInput.files[0];
    if (!file) return;
    uploadAssistantAudio(file);
}

function uploadAssistantAudio(fileBlob) {
    assistantHint.innerText = "Analyzing voice command...";
    btnAssistantRecord.disabled = true;
    btnAssistantUploadTrigger.disabled = true;

    // Reset telemetry inputs
    tTranscription.innerText = "Transcribing...";
    tIntent.innerText = "-";
    tEntity.innerText = "-";
    tConfidence.innerText = "-";
    tVerification.innerText = "-";
    assistantActionFeedback.innerText = "Processing pipeline...";
    const logBox = document.querySelector(".execution-log-box");
    if (logBox) {
        logBox.className = "execution-log-box";
    }

    const formData = new FormData();
    formData.append("audio", fileBlob, "command.wav");

    fetch("/api/voice-command", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        btnAssistantRecord.disabled = false;
        btnAssistantUploadTrigger.disabled = false;
        assistantHint.innerText = "Command analysis completed.";

        if (!data.success) {
            assistantActionFeedback.innerText = "Error: " + data.error;
            if (logBox) logBox.className = "execution-log-box rejected";
            
            if (data.voice_response) {
                speakAssistantResponse(data.voice_response);
            }
            return;
        }

        // Render Telemetry
        tTranscription.innerText = `"${data.transcription}"`;
        tIntent.innerText = data.intent;
        tEntity.innerText = data.entity ? data.entity.toUpperCase() : "NONE";
        tConfidence.innerText = `${(data.confidence * 100).toFixed(0)}%`;
        
        const authRole = data.authenticated ? "Verified Adult" : "Child User";
        tVerification.innerText = `${data.voice_age_class} (${authRole})`;
        tVerification.style.color = data.authenticated ? "var(--primary)" : "var(--danger)";

        // Render feedback box
        assistantActionFeedback.innerText = data.action_status;
        if (logBox) {
            if (data.action_status.startsWith("Rejected")) {
                logBox.className = "execution-log-box rejected";
            } else {
                logBox.className = "execution-log-box authenticated";
            }
        }

        // Add to history list UI
        addCommandToHistory(data.transcription, data.intent, data.action_status);

        // Sync protection status UI header
        if (data.protection_enabled !== undefined) {
            isProtectionEnabled = data.protection_enabled;
            const statusDot = document.getElementById("assistant-status-dot");
            const statusText = document.getElementById("assistant-status-text");
            
            if (isProtectionEnabled) {
                statusDot.className = "status-dot green";
                statusText.innerText = "Parental Control: Enabled";
            } else {
                statusDot.className = "status-dot red";
                statusText.innerText = "Parental Control: Disabled";
            }
        }

        // Sync custom blocked apps and trigger store grid render
        if (data.blocked_apps !== undefined) {
            customBlockedApps = data.blocked_apps.map(app => {
                const cleanApp = app.toLowerCase().trim();
                return ENTITY_TO_ID[cleanApp] || cleanApp;
            });
            renderApps();
        }

        // Open application if requested by OPEN_APP intent
        if (data.intent === "OPEN_APP" && data.entity) {
            const cleanApp = data.entity.toLowerCase().trim();
            const targetId = ENTITY_TO_ID[cleanApp] || cleanApp;
            const targetApp = APPS.find(app => 
                app.id === targetId || 
                app.name.toLowerCase() === cleanApp ||
                app.name.toLowerCase().includes(cleanApp)
            );
            
            if (targetApp) {
                const isRestricted = isProtectionEnabled && 
                                     (targetApp.isRestricted || customBlockedApps.includes(targetApp.id)) && 
                                     currentAgeGroup === "Below 18";
                setTimeout(() => {
                    handleAppClick(targetApp, isRestricted);
                }, 800);
            } else {
                console.warn("Application entity not found in APPS list:", data.entity);
            }
        }

        // Read out loud TTS response
        speakAssistantResponse(data.voice_response);
    })
    .catch(err => {
        console.error(err);
        assistantHint.innerText = "API Request failed.";
        btnAssistantRecord.disabled = false;
        btnAssistantUploadTrigger.disabled = false;
        assistantActionFeedback.innerText = "Error contacting voice server.";
        if (logBox) logBox.className = "execution-log-box rejected";
    });
}

function addCommandToHistory(transcription, intent, status) {
    const list = assistantHistoryList;
    const emptyEl = list.querySelector(".empty");
    if (emptyEl) {
        list.innerHTML = "";
    }

    const li = document.createElement("li");
    li.className = "history-item";
    li.innerHTML = `<strong>Cmd:</strong> "${transcription}"<br>
                    <span style="font-size:0.7rem; color:var(--text-muted)">Intent: ${intent} | Status: ${status}</span>`;
    
    // Insert at top of list
    list.insertBefore(li, list.firstChild);

    // Limit to last 5 entries
    while (list.children.length > 5) {
        list.removeChild(list.lastChild);
    }
}

function speakAssistantResponse(text) {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        window.speechSynthesis.speak(utterance);
    }
}

function drawAssistantVoiceIdle() {
    assistantVisualizerCtx.clearRect(0, 0, assistantVisualizer.width, assistantVisualizer.height);
    assistantVisualizerCtx.strokeStyle = "rgba(148, 163, 184, 0.2)";
    assistantVisualizerCtx.lineWidth = 2;
    assistantVisualizerCtx.beginPath();
    assistantVisualizerCtx.moveTo(0, assistantVisualizer.height / 2);
    assistantVisualizerCtx.lineTo(assistantVisualizer.width, assistantVisualizer.height / 2);
    assistantVisualizerCtx.stroke();
}

function drawAssistantVoiceLive() {
    if (!assistantIsRecording || !assistantAnalyserNode) return;
    requestAnimationFrame(drawAssistantVoiceLive);
    
    const bufferLength = assistantAnalyserNode.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    assistantAnalyserNode.getByteTimeDomainData(dataArray);
    
    assistantVisualizerCtx.fillStyle = "rgba(11, 14, 20, 0.4)";
    assistantVisualizerCtx.fillRect(0, 0, assistantVisualizer.width, assistantVisualizer.height);
    
    assistantVisualizerCtx.lineWidth = 3;
    assistantVisualizerCtx.strokeStyle = "var(--secondary)";
    assistantVisualizerCtx.beginPath();
    
    const sliceWidth = assistantVisualizer.width * 1.0 / bufferLength;
    let x = 0;
    
    for (let i = 0; i < bufferLength; i++) {
        const v = dataArray[i] / 128.0;
        const y = v * assistantVisualizer.height / 2;
        
        if (i === 0) {
            assistantVisualizerCtx.moveTo(x, y);
        } else {
            assistantVisualizerCtx.lineTo(x, y);
        }
        x += sliceWidth;
    }
    
    assistantVisualizerCtx.lineTo(assistantVisualizer.width, assistantVisualizer.height / 2);
    assistantVisualizerCtx.stroke();
}

function syncPortalState() {
    fetch("/api/status")
    .then(res => res.json())
    .then(data => {
        if (data.blocked_apps !== undefined) {
            customBlockedApps = data.blocked_apps.map(app => {
                const cleanApp = app.toLowerCase().trim();
                return ENTITY_TO_ID[cleanApp] || cleanApp;
            });
        }
        if (data.protection_enabled !== undefined) {
            isProtectionEnabled = data.protection_enabled;
            const statusDot = document.getElementById("assistant-status-dot");
            const statusText = document.getElementById("assistant-status-text");
            if (statusDot && statusText) {
                if (isProtectionEnabled) {
                    statusDot.className = "status-dot green";
                    statusText.innerText = "Parental Control: Enabled";
                } else {
                    statusDot.className = "status-dot red";
                    statusText.innerText = "Parental Control: Disabled";
                }
            }
        }
        renderApps();
    })
    .catch(err => console.error("Error syncing portal state:", err));
}
