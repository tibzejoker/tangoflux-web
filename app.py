from flask import Flask, render_template, request, session, jsonify, url_for, send_file
import os
import uuid
import torchaudio
from tangoflux import TangoFluxInference
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Configuration
UPLOAD_FOLDER = "generated_sounds"
SECRET_KEY = "your_secret_key"
MAX_GENERATIONS = 10  # Maximum number of sounds that can be generated at once
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Cleanup on server start
for file in os.listdir(UPLOAD_FOLDER):
    os.remove(os.path.join(UPLOAD_FOLDER, file))

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Load the TangoFlux model
model = TangoFluxInference(name="declare-lab/TangoFlux")
executor = ThreadPoolExecutor(max_workers=3)  # Limit concurrent generations

@app.route("/")
def index():
    # Create a session ID if it doesn't exist
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
    # Reverse the generated sounds list for newest-first order
    sounds = session.get("generated_sounds", [])[::-1]
    return render_template("index.html", sounds=sounds)

def generate_single_sound(prompt, duration, user_id):
    """Helper function to generate a single sound file"""
    # Generate unique filename
    filename = f"{user_id}_{uuid.uuid4().hex}.wav"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    try:
        # Generate sound
        audio = model.generate(prompt, steps=50, duration=duration)
        torchaudio.save(filepath, audio, 44100)
        
        return {
            "filename": filename,
            "prompt": prompt,
            "url": url_for("static", filename=f"sounds/{filename}")
        }
    except Exception as e:
        # Clean up file if it was created
        if os.path.exists(filepath):
            os.remove(filepath)
        raise e  # Re-raise the exception to be handled by the route

@app.route("/generate", methods=["POST"])
def generate():
    print("Received form data:", request.form)  # Debug print
    print("Files:", request.files)  # Debug print
    
    try:
        # Extract and validate input parameters
        prompt = request.form.get("prompt")
        duration = request.form.get("duration")
        quantity = request.form.get("quantity", 1)
        
        print(f"Parsed values - prompt: {prompt}, duration: {duration}, quantity: {quantity}")
        
        # Validate presence of required fields
        if not prompt:
            return jsonify({"error": "Missing prompt"}), 400
            
        # Convert and validate numeric fields
        try:
            duration = int(duration)
            quantity = int(quantity)
        except (TypeError, ValueError):
            return jsonify({"error": "Duration and quantity must be numbers"}), 400
            
        # Validate ranges
        if not (1 <= duration <= 30):
            return jsonify({"error": "Duration must be between 1 and 30 seconds"}), 400
            
        if not (1 <= quantity <= MAX_GENERATIONS):
            return jsonify({"error": f"Quantity must be between 1 and {MAX_GENERATIONS}"}), 400

        # Generate unique filename
        filename = f"{session['user_id']}_{uuid.uuid4().hex}.wav"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        try:
            # Generate the sound
            audio = model.generate(prompt, steps=50, duration=duration)
            torchaudio.save(filepath, audio, 44100)
            
            # Generate the response data
            sound_data = {
                "filename": filename,
                "prompt": prompt,
                "url": f"/static/sounds/{filename}"  # Direct URL construction
            }

            # Update session data
            if "generated_sounds" not in session:
                session["generated_sounds"] = []
            
            session["generated_sounds"].append({
                "filename": filename, 
                "prompt": prompt
            })
            session.modified = True

            return jsonify(sound_data)

        except Exception as e:
            # Clean up file if it was created
            if os.path.exists(filepath):
                os.remove(filepath)
            raise e

    except Exception as e:
        app.logger.error(f"Error generating sound: {str(e)}")
        return jsonify({"error": "Failed to generate sound: " + str(e)}), 500
    


@app.route("/static/sounds/<filename>")
def serve_audio(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404
    return send_file(filepath, mimetype='audio/wav')

setup_done = False  # Add a global flag to track setup completion

@app.before_request
def cleanup_session():
    global setup_done
    if not setup_done:
        if "generated_sounds" in session:
            # Clean up missing files from session
            session["generated_sounds"] = [
                sound for sound in session["generated_sounds"]
                if os.path.exists(os.path.join(UPLOAD_FOLDER, sound["filename"]))
            ]
            session.modified = True
            
            # Cleanup old files if too many
            user_files = [
                f for f in os.listdir(UPLOAD_FOLDER)
                if f.startswith(session["user_id"])
            ]
            if len(user_files) > 50:  # Keep max 50 files per user
                user_files.sort(key=lambda x: os.path.getctime(
                    os.path.join(UPLOAD_FOLDER, x)
                ))
                for old_file in user_files[:-50]:
                    try:
                        os.remove(os.path.join(UPLOAD_FOLDER, old_file))
                    except OSError:
                        pass
        setup_done = True

# Error handlers
@app.errorhandler(413)  # Payload Too Large
def request_entity_too_large(error):
    return jsonify({"error": "Request too large"}), 413

@app.errorhandler(429)  # Too Many Requests
def too_many_requests(error):
    return jsonify({"error": "Too many requests"}), 429

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5566, debug=True)