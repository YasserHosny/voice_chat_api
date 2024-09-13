from flask import Blueprint, request, jsonify
from app.services.voice_service import process_voice_file
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