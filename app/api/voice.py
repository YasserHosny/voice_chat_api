from flask import Blueprint, request, jsonify, send_file, url_for
from app.services.voice_service import process_voice_file
import requests
import os
import subprocess
from config import config
from io import BytesIO
import zipfile

# from docling.document_converter import DocumentConverter

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

# New endpoint for converting a PDF or URL to markdown
# @voice_bp.route('/convert-pdf', methods=['POST'])
# def convert_pdf():
#     print("Received request to convert PDF.")

#     # Get the PDF source (can be a URL or a file path)
#     data = request.get_json()
#     source = data.get('source')

#     if not source:
#         return jsonify({"error": "No source provided."}), 400

#     try:
#         # Use DocumentConverter to convert the PDF
#         converter = DocumentConverter()
#         result = converter.convert_single(source)

#         # Render as markdown
#         markdown_result = result.render_as_markdown()
#         print("PDF conversion successful.")
#         return jsonify({"markdown": markdown_result})

#     except Exception as e:
#         print(f"Error converting PDF: {str(e)}")
#         return jsonify({"error": f"Failed to convert PDF. {str(e)}"}), 500

# New endpoint for sending a PDF to an external API
@voice_bp.route('/send-pdf', methods=['POST'])
def send_pdf():
    print("Received request to send PDF to external API.")
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        # Define the external API URL
        url = "https://www.datalab.to/api/v1/marker"
        
        # Prepare form data
        form_data = {
            'file': (file.filename, file, 'application/pdf'),
            'langs': (None, "English"),
            "force_ocr": (None, False),
            "paginate": (None, False)
        }
        
        # Set headers (replace 'YOUR_API_KEY' with your actual API key)
        headers = {"X-Api-Key": config.MARKER_PDF_API}
        
        # Send the request to the external API
        response = requests.post(url, files=form_data, headers=headers)
        
        # Check for a successful response
        if response.status_code == 200:
            data = response.json()
            print("External API response received:", data)
            return jsonify(data)
        else:
            print(f"External API error: {response.status_code} - {response.text}")
            return jsonify({"error": f"Failed to send PDF to external API. Status code: {response.status_code}"}), 500

    except Exception as e:
        print(f"Error sending PDF to external API: {str(e)}")
        return jsonify({"error": f"Error occurred: {str(e)}"}), 500
    
voice_bp = Blueprint('voice_bp', __name__)

# Ensure the 'result' folder exists in your app
RESULT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'result')
os.makedirs(RESULT_FOLDER, exist_ok=True)

@voice_bp.route('/marker-pdf', methods=['POST'])
def marker_pdf():
    print("Received request to process PDF using marker tool.")
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file to the 'result' folder
    try:
        input_pdf_path = os.path.join(RESULT_FOLDER, file.filename)
        output_folder = os.path.join(RESULT_FOLDER, 'output')

        # Save the file locally in the result folder
        file.save(input_pdf_path)
        print(f"File saved at {input_pdf_path}")

        # Ensure the output folder exists in the result folder
        os.makedirs(output_folder, exist_ok=True)

        # Run the marker_single command with subprocess
        command = [
            "marker_single",
            input_pdf_path,
            output_folder,
            "--batch_multiplier", "2",
            "--max_pages", "10"
        ]
        print(f"Running command: {' '.join(command)}")

        # Execute the command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Capture output and errors
        if result.returncode == 0:
            print("Marker tool executed successfully.")
            
            # Find the .md file in the output folder
            md_file_path = None
            for root, dirs, files in os.walk(output_folder):
                for file in files:
                    if file.endswith('.md'):
                        md_file_path = os.path.join(root, file)
                        break

            # Check if the .md file was found
            if md_file_path and os.path.exists(md_file_path):
                # Move the .md file to the result folder for easier access
                md_filename = os.path.basename(md_file_path)
                markdown_output_path = os.path.join(RESULT_FOLDER, md_filename)
                os.rename(md_file_path, markdown_output_path)
                print(f"Markdown file moved to {markdown_output_path}")
            else:
                print("Markdown file not found.")
                markdown_output_path = None
            
            # Create a zip archive of the output folder
            zip_filename = "output.zip"
            zip_buffer = BytesIO()

            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for root, dirs, files in os.walk(output_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zip_file.write(file_path, os.path.relpath(file_path, output_folder))
            
            zip_buffer.seek(0)

            # Save the zip file locally so that the user can download it
            zip_download_path = os.path.join(RESULT_FOLDER, zip_filename)
            with open(zip_download_path, 'wb') as f:
                f.write(zip_buffer.getvalue())

            # Create URLs for downloading the zip and markdown files
            zip_download_url = url_for('voice_bp.download_zip', filename=zip_filename, _external=True)
            markdown_url = url_for('voice_bp.download_md', filename=md_filename, _external=True) if markdown_output_path else None

            # Return the URLs for both the markdown file and zip file
            return jsonify({
                "markdown_url": markdown_url,  # Download link for the .md file
                "zip_download_url": zip_download_url  # Download link for the zip file
            })

        else:
            print(f"Marker tool failed with error: {result.stderr.decode('utf-8')}")
            return jsonify({"error": result.stderr.decode('utf-8')}), 500

    except Exception as e:
        print(f"Error processing PDF with marker tool: {str(e)}")
        return jsonify({"error": f"Error occurred: {str(e)}"}), 500

@voice_bp.route('/download-zip/<filename>', methods=['GET'])
def download_zip(filename):
    try:
        zip_path = os.path.join(RESULT_FOLDER, filename)
        if os.path.exists(zip_path):
            return send_file(zip_path, mimetype='application/zip', as_attachment=True, download_name=filename)
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@voice_bp.route('/download-md/<filename>', methods=['GET'])
def download_md(filename):
    try:
        md_path = os.path.join(RESULT_FOLDER, filename)
        if os.path.exists(md_path):
            return send_file(md_path, mimetype='text/markdown', as_attachment=False)
        else:
            return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500