import os
import tempfile
from flask import Flask, request, jsonify, send_from_directory, render_template, session
import inference
import config
import speech_recognition as sr
import nlp_module

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = "voicevision_parental_control_key_2026"

# Ensure static and template folders exist
os.makedirs(os.path.join(config.BASE_DIR, "static"), exist_ok=True)
os.makedirs(os.path.join(config.BASE_DIR, "templates"), exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def predict_age():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
        
    audio_file = request.files["audio"]
    if audio_file.filename == "":
        return jsonify({"error": "Empty audio file"}), 400

    # Save to a temporary file inside the workspace
    temp_dir = os.path.join(config.BASE_DIR, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, "upload_recording.wav")
    
    try:
        audio_file.save(temp_path)
        
        # Run age prediction
        result = inference.predict_age_group(temp_path)
        
        # Add success status
        result["success"] = True
        return jsonify(result)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500
        
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

@app.route("/api/samples", methods=["GET"])
def list_samples():
    """
    List pre-recorded demonstration samples available in the directory.
    """
    sample_files = ["boy1.mp3", "boy3.mp3", "girl1.mp3"]
    samples_list = []
    
    for filename in sample_files:
        path = os.path.join(config.BASE_DIR, filename)
        if os.path.exists(path):
            # We determine class based on filename to help UI display labels for test selection
            expected_class = "Below 18" if ("boy" in filename or "girl" in filename) else "18 or Above"
            samples_list.append({
                "filename": filename,
                "label": f"Sample: {filename} ({expected_class})"
            })
            
    return jsonify(samples_list)

@app.route("/api/samples/<filename>", methods=["GET"])
def get_sample(filename):
    """
    Serve a sample file for playback or classification.
    """
    return send_from_directory(config.BASE_DIR, filename)

@app.route("/api/predict-sample/<filename>", methods=["POST"])
def predict_sample(filename):
    """
    Directly evaluate one of the local sample files on the backend.
    """
    path = os.path.join(config.BASE_DIR, filename)
    if not os.path.exists(path):
        return jsonify({"error": "Sample file not found"}), 404
        
    try:
        result = inference.predict_age_group(path)
        result["success"] = True
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/predict-face", methods=["POST"])
def predict_face():
    """
    Accept an uploaded face image and run the age prediction pipeline.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400
        
    image_file = request.files["image"]
    if image_file.filename == "":
        return jsonify({"error": "Empty image file"}), 400

    temp_dir = os.path.join(config.BASE_DIR, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, "upload_face.jpg")
    
    try:
        image_file.save(temp_path)
        
        # Run face age prediction
        import customized_testing_phase
        result = customized_testing_phase.predict_face_age(temp_path)
        return jsonify(result)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500
        
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

@app.route("/temp_faces/<path:filename>", methods=["GET"])
def serve_temp_face(filename):
    """
    Serve cropped face crop images generated during prediction.
    """
    temp_dir = os.path.join(config.BASE_DIR, "temp_faces")
    return send_from_directory(temp_dir, filename)

# Low-risk intents that do not require parent authorization
LOW_RISK_INTENTS = ["OPEN_PORTAL", "CHECK_STATUS", "VIEW_BLOCKED_APPS", "VIEW_ACCESS_HISTORY", "HELP", "CHECK_AGE", "OPEN_APP"]

@app.route("/api/voice-command", methods=["POST"])
def voice_command():
    """
    Process incoming voice commands, perform Speech-To-Text, run biometric age 
    authentication, execute NLP intent classification, and execute parental actions.
    """
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
        
    audio_file = request.files["audio"]
    if audio_file.filename == "":
        return jsonify({"error": "Empty audio file"}), 400

    temp_dir = os.path.join(config.BASE_DIR, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, "command_recording.wav")
    
    try:
        audio_file.save(temp_path)
        
        # Convert audio to standard PCM WAV format using librosa + soundfile
        wav_path = os.path.join(temp_dir, "command_pcm.wav")
        import librosa
        import soundfile as sf
        y, sr_rate = librosa.load(temp_path, sr=16000)
        sf.write(wav_path, y, sr_rate, subtype='PCM_16')
        
        # 1. Speech-to-Text (STT)
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            
        transcription = ""
        try:
            transcription = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return jsonify({
                "success": False,
                "error": "Speech was not clear. Please speak again.",
                "voice_response": "I could not understand what you said. Please speak again."
            })
        except sr.RequestError:
            # Fallback based on transcription failure
            return jsonify({
                "success": False,
                "error": "Speech recognition service is currently unavailable.",
                "voice_response": "Speech recognition service is offline."
            })

        if not transcription.strip():
            return jsonify({
                "success": False,
                "error": "No speech detected.",
                "voice_response": "I didn't hear anything. Please speak again."
            })

        # 2. Voice-Based Age Verification (Biometric Auth)
        voice_age_result = inference.predict_age_group(temp_path)
        is_adult = (voice_age_result["predicted_class"] == "18 or Above")
        
        # Retrieve context from session
        last_listed_apps = session.get("last_listed_apps", [])
        
        # 3. NLP Intent Classification & Entity Extraction
        nlp_res = nlp_module.predict_intent(transcription, last_listed_apps)
        intent = nlp_res["intent"]
        entity = nlp_res["entity"]
        confidence = nlp_res["confidence"]
        clarification_needed = nlp_res["clarification_needed"]
        
        # Clarification handling
        if clarification_needed:
            return jsonify({
                "success": True,
                "transcription": transcription,
                "intent": intent,
                "entity": entity,
                "confidence": confidence,
                "authenticated": is_adult,
                "voice_age_class": voice_age_result["predicted_class"],
                "clarification_needed": True,
                "voice_response": f"I'm not sure what you mean by '{transcription}'. Can you please clarify?",
                "action_status": "Clarification requested."
            })

        # 4. Permission & Authentication Check
        is_high_risk = intent not in LOW_RISK_INTENTS
        authenticated = is_adult
        
        if is_high_risk and not authenticated:
            return jsonify({
                "success": True,
                "transcription": transcription,
                "intent": intent,
                "entity": entity,
                "confidence": confidence,
                "authenticated": False,
                "voice_age_class": voice_age_result["predicted_class"],
                "voice_response": "You do not have access to do that.",
                "action_status": "Rejected: You do not have access to do that."
            })

        # 5. Command Execution
        action_status = "Executed successfully."
        voice_response = "Action completed."
        
        if "blocked_apps" not in session:
            session["blocked_apps"] = ["youtube", "instagram"]
            
        blocked_apps = list(session["blocked_apps"])
        
        if intent == "OPEN_PORTAL":
            voice_response = "Launching parental control portal dashboard."
            action_status = "Portal opened."
            
        elif intent == "CHECK_STATUS":
            status_str = "enabled" if session.get("protection_enabled", True) else "disabled"
            voice_response = f"Parental protection is currently {status_str}."
            action_status = f"Status checked: {status_str}."
            
        elif intent == "ENABLE_PROTECTION":
            session["protection_enabled"] = True
            voice_response = "Parental control protection has been enabled."
            action_status = "Protection enabled."
            
        elif intent == "DISABLE_PROTECTION":
            session["protection_enabled"] = False
            voice_response = "Parental control protection has been disabled."
            action_status = "Protection disabled."
            
        elif intent == "BLOCK_APP":
            if not entity:
                return jsonify({
                    "success": True,
                    "transcription": transcription,
                    "intent": intent,
                    "entity": None,
                    "confidence": confidence,
                    "authenticated": True,
                    "voice_age_class": "18 or Above",
                    "voice_response": "Which application would you like to block?",
                    "action_status": "App name entity missing."
                })
            if entity not in blocked_apps:
                blocked_apps.append(entity)
                session["blocked_apps"] = blocked_apps
            voice_response = f"{entity.capitalize()} has been successfully blocked."
            action_status = f"{entity.capitalize()} blocked."
            
        elif intent == "UNBLOCK_APP":
            if not entity:
                return jsonify({
                    "success": True,
                    "transcription": transcription,
                    "intent": intent,
                    "entity": None,
                    "confidence": confidence,
                    "authenticated": True,
                    "voice_age_class": "18 or Above",
                    "voice_response": "Which application would you like to unblock?",
                    "action_status": "App name entity missing."
                })
            if entity in blocked_apps:
                blocked_apps.remove(entity)
                session["blocked_apps"] = blocked_apps
            voice_response = f"{entity.capitalize()} has been successfully unblocked."
            action_status = f"{entity.capitalize()} unblocked."
            
        elif intent == "VIEW_BLOCKED_APPS":
            if blocked_apps:
                app_list_str = " and ".join([a.capitalize() for a in blocked_apps])
                voice_response = f"Currently blocked applications are {app_list_str}."
                action_status = f"Blocked list: {app_list_str}."
                session["last_listed_apps"] = blocked_apps
            else:
                voice_response = "No applications are currently blocked."
                action_status = "Blocked list empty."
                session["last_listed_apps"] = []
                
        elif intent == "VIEW_ACCESS_HISTORY":
            logs = ["Chrome opened at 10:15 AM", "Minecraft blocked at 11:30 AM", "YouTube blocked at 1:45 PM"]
            voice_response = "Showing access history log details."
            action_status = ", ".join(logs)
            
        elif intent == "CHECK_AGE":
            voice_response = f"Voice analysis indicates you are in the {voice_age_result['predicted_class']} age category."
            action_status = f"Speaker age predicted: {voice_age_result['predicted_class']}."
            
        elif intent == "VERIFY_USER":
            role = "Verified Adult Parent" if authenticated else "Child User"
            voice_response = f"Speaker verification completed. Role identified as {role}."
            action_status = f"Verification role: {role}."
            
        elif intent == "OPEN_SETTINGS":
            voice_response = "Opening parental control configurations settings panel."
            action_status = "Settings panel loaded."
            
        elif intent == "HELP":
            voice_response = "You can say commands like block YouTube, check protection status, or view blocked applications."
            action_status = "Help commands listed."
            
        elif intent == "EXIT":
            voice_response = "Closing dashboard portal."
            action_status = "Portal closed."
            
        elif intent == "OPEN_APP":
            if not entity:
                return jsonify({
                    "success": True,
                    "transcription": transcription,
                    "intent": intent,
                    "entity": None,
                    "confidence": confidence,
                    "authenticated": authenticated,
                    "voice_age_class": voice_age_result["predicted_class"],
                    "voice_response": "Which application would you like to open?",
                    "action_status": "App name entity missing."
                })
            voice_response = f"Opening {entity.capitalize()}."
            action_status = f"Opening {entity.capitalize()}..."
            
        return jsonify({
            "success": True,
            "transcription": transcription,
            "intent": intent,
            "entity": entity,
            "confidence": confidence,
            "authenticated": authenticated,
            "voice_age_class": voice_age_result["predicted_class"],
            "action_status": action_status,
            "voice_response": voice_response,
            "blocked_apps": blocked_apps,
            "protection_enabled": session.get("protection_enabled", True)
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500
        
    finally:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
        if 'wav_path' in locals() and os.path.exists(wav_path):
            try:
                os.remove(wav_path)
            except Exception:
                pass

@app.route("/api/status", methods=["GET"])
def get_status():
    """
    Exposes active session parameters (blocked apps and enabled status) 
    to synchronize portal client state.
    """
    if "blocked_apps" not in session:
        session["blocked_apps"] = ["youtube", "instagram"]
    return jsonify({
        "blocked_apps": list(session["blocked_apps"]),
        "protection_enabled": session.get("protection_enabled", True)
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
