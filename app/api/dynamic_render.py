from flask import Blueprint, request, jsonify
from app.services.dynamic_render_service import process_chat_text

dynamic_render_bp = Blueprint('dynamic_render', __name__)

class DynamicRenderAPI:
    
    @dynamic_render_bp.route('/component_chat', methods=['POST'])
    def dynamic_render():
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400

        chat_text = data.get('chat_text', '')

        # Process chat text using the service
        result = process_chat_text(chat_text)

        # Simulate dynamic Angular component render
        angular_component = f"<app-dynamic-component [input]='{result['response']}'></app-dynamic-component>"

        return jsonify({'rendered_component': angular_component})