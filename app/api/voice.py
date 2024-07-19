from flask import Blueprint, request, jsonify
from app.services.voice_service import process_voice_file

voice_bp = Blueprint('voice_bp', __name__)

@voice_bp.route('/process', methods=['POST'])
def process_voice():
    print("Received request to process voice file.")
    if 'file' not in request.files:
        print("No file part in the request.")
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        print("No selected file.")
        return jsonify({"error": "No selected file"}), 400

    print("Processing file:", file.filename)
    response = process_voice_file(file)
    print("File processed. Response:", response)
    return jsonify(response)

