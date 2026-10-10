import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Predefined known applications for entity extraction
KNOWN_APPS = [
    "duolingo", "youtube kids", "sketchbook", "abc mouse", "minecraft", 
    "roblox", "scratch", "teams", "subway surfers", "khan academy", 
    "instagram", "youtube", "facebook", "x", "telegram", "reddit", 
    "discord", "snapchat", "fiverr", "gpay", "phonepe", "steam chat", 
    "twitch", "linkedin", "indeed", "chrome"
]

# Map synonyms or variations to canonical app names
APP_SYNONYMS = {
    "yt": "youtube",
    "yt kids": "youtube kids",
    "google pay": "gpay",
    "phone pe": "phonepe",
    "twitter": "x",
    "teams app": "teams",
    "autodesk": "sketchbook",
    "steam": "steam chat"
}

# Predefined intents and varied examples for training the classifier
INTENT_DATA = {
    "OPEN_PORTAL": [
        "open voicevision", "launch the parental control portal", "go to portal", 
        "open dashboard", "launch website", "open the app", "launch app", "open interface",
        "open parent panel", "show portal", "load dashboard", "display gate"
    ],
    "CHECK_STATUS": [
        "what is the protection status", "show protection status", "is parental control active", 
        "check security status", "status check", "is it active", "what's the current protection status",
        "are apps restricted right now", "check status", "is protection enabled", "protection status"
    ],
    "ENABLE_PROTECTION": [
        "turn on protection", "enable parental control", "activate safety", "start monitoring", 
        "enable protection", "turn on safety mode", "lock down apps", "restrict access now",
        "turn protection on", "activate parental control", "enable restriction"
    ],
    "DISABLE_PROTECTION": [
        "turn off protection", "disable parental control", "stop monitoring", "deactivate protection", 
        "turn off safety mode", "remove protection", "disable gate", "deactivate restriction",
        "turn protection off", "deactivate safety mode", "stop security monitoring"
    ],
    "BLOCK_APP": [
        "block youtube", "please restrict instagram", "prevent access to facebook", "restrict twitch", 
        "lock tiktok", "block access to reddit", "stop access to snapchat", "block chrome",
        "restrict youtube access", "prevent access to instagram", "ban discord", "disable steam chat"
    ],
    "UNBLOCK_APP": [
        "unblock youtube", "please allow instagram again", "remove restriction on facebook", 
        "unblock chrome", "unlock youtube", "allow youtube", "allow instagram", "unban discord",
        "remove block from snapchat", "open up roblox", "enable reddit access", "unblock steam chat"
    ],
    "CHECK_AGE": [
        "check my age", "verify age", "what age group do I belong to", "predict my age", 
        "am I below eighteen", "what is my age category", "check user age", "classify my age",
        "predict age group", "am i minor", "am i adult"
    ],
    "VERIFY_USER": [
        "verify user", "authenticate me", "confirm my voice", "verify parent", 
        "am I authenticated", "run authentication check", "verify my identity", "parent verification",
        "confirm adult profile", "run voice authentication"
    ],
    "VIEW_BLOCKED_APPS": [
        "show me the blocked applications", "list restricted apps", "what apps are currently blocked", 
        "show blocked list", "view blocked apps", "which apps are locked", "show me restricted apps",
        "list blocked programs", "show locked applications", "what is blocked"
    ],
    "VIEW_ACCESS_HISTORY": [
        "show access history", "view logs", "list connection history", "show the access history for chrome", 
        "view access log", "show connection logs", "what apps were opened recently", "view access history",
        "show list of opened apps", "history log"
    ],
    "OPEN_SETTINGS": [
        "open parental settings", "go to settings", "modify control options", "open settings", 
        "configure settings", "show settings panel", "change options", "settings menu"
    ],
    "HELP": [
        "what commands can I use", "help me", "show commands list", "what can I say", "help", 
        "commands support", "list commands", "how do I use voice commands", "show menu"
    ],
    "EXIT": [
        "exit portal", "close window", "quit app", "exit", "quit", "close dashboard", 
        "close interface", "shutdown portal", "go away"
    ],
    "OPEN_APP": [
        "open youtube", "launch instagram", "start minecraft", "open roblox", "run chrome",
        "open duolingo", "launch voicevision app teams", "open fiverr", "start scratch", 
        "open gpay", "launch phonepe", "open teams", "open subway surfers", "open khan academy", 
        "open sketchbook", "open facebook", "open x", "open telegram", "open reddit", "open discord",
        "open snapchat", "open steam chat", "open twitch", "open linkedin", "open indeed", "launch youtube kids"
    ]
}

# Fit TF-IDF Vectorizer and Logistic Regression Classifier on startup
X = []
y = []
for intent, phrases in INTENT_DATA.items():
    for phrase in phrases:
        normalized = phrase.lower().strip()
        X.append(normalized)
        y.append(intent)

vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X_vec = vectorizer.fit_transform(X)
classifier = LogisticRegression(C=5.0)
classifier.fit(X_vec, y)

def normalize_text(text):
    """Normalize input text by removing punctuation, converting to lower case, and stripping spaces."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_app_entity(text):
    """Extract known application entity and resolve synonyms."""
    words = text.split()
    # Check multi-word app names first
    for app in KNOWN_APPS:
        if app in text:
            return app
            
    # Check synonyms
    for syn, canonical in APP_SYNONYMS.items():
        if syn in text:
            return canonical
            
    # Check single words
    for word in words:
        if word in KNOWN_APPS:
            return word
        if word in APP_SYNONYMS:
            return APP_SYNONYMS[word]
            
    return None

def resolve_context_entity(text, last_listed_apps):
    """Resolves index words like 'first', 'second', 'last', 'it' to the last listed apps list."""
    if not last_listed_apps:
        return None
        
    normalized = normalize_text(text)
    if "first" in normalized:
        return last_listed_apps[0]
    elif "second" in normalized:
        if len(last_listed_apps) > 1:
            return last_listed_apps[1]
    elif "third" in normalized:
        if len(last_listed_apps) > 2:
            return last_listed_apps[2]
    elif "last" in normalized:
        return last_listed_apps[-1]
    elif "it" in normalized or "that" in normalized or "this" in normalized:
        return last_listed_apps[0]
        
    return None

def predict_intent(raw_text, last_listed_apps=None):
    """Predicts the intent of a raw user speech query and extracts relevant entities."""
    normalized_text = normalize_text(raw_text)
    if not normalized_text:
        return {
            "intent": "UNKNOWN",
            "entity": None,
            "confidence": 0.0,
            "clarification_needed": True,
            "normalized_text": ""
        }

    # Vectorize and predict
    vec = vectorizer.transform([normalized_text])
    probs = classifier.predict_proba(vec)[0]
    pred_idx = np.argmax(probs)
    intent = classifier.classes_[pred_idx]
    confidence = float(probs[pred_idx])

    # Extract App Entity
    entity = extract_app_entity(normalized_text)
    
    # Resolve context if no direct app was found
    if not entity and last_listed_apps:
        entity = resolve_context_entity(normalized_text, last_listed_apps)

    # Threshold check for low-confidence clarification
    clarification_needed = confidence < 0.60

    return {
        "intent": intent,
        "entity": entity,
        "confidence": confidence,
        "clarification_needed": clarification_needed,
        "normalized_text": normalized_text
    }
