from flask import Blueprint, request, jsonify, Response
from app.services.dynamic_render_service import process_chat_text, extract_life_cycle_status, extract_json_response

dynamic_render_bp = Blueprint('dynamic_render', __name__)

class DynamicRenderAPI:
    @dynamic_render_bp.route('/component_chat', methods=['POST'])
    def dynamic_render():
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Invalid JSON'}), 400

        chat_text = data.get('chat_text', '')

        prompt = """
Given the following user question:  

**User Question:** "{user_question}"  

Ingore any previous conversation, then classify it into one of the following business domains and extract the relevant parameters:

1. **Product Portfolio**: The user is asking about drawing a product categories chart for the "product portfolio" domain.
   - **Filters:**
     - **Life Cycle Status**: Extract values from ["Active", "EOL", "Unconfirmed"]. If multiple values are mentioned, include them in a list.
     - **RoHS Status**: Extract values from ["Compliant", "Not Compliant", "Unknown"]. If multiple values are mentioned, include them in a list.
   - **Scope**: Extract if the user requests "Top 10" or "All" categories.

2. **Cross Summary**: The user is asking about drawing a product categories chart for the "cross summary" domain.
   - **Filters:**
     - **Life Cycle Status**: Extract one of ["Active_To_Active", "EOL", "Active_To_Obsolete", "Obsolete_To_Active", "ALL"].
   - **Scope**: Extract if the user requests "Top 10" or "All" categories.

Return the result **ONLY** in the following JSON format without additional explanations:

**Example 1:**
```json
{{ 
    "businessDomain": "product_portfolio", 
    "rohsStatuses": [
        "Compliant",
        "Not Compliant",
        "Unknown"
    ],
    "lifecycleStatuses": [
        "Active",
        "EOL",
        "Unconfirmed"
    ],
    "Scope": "Top 10"
}}
Example 2:
{{
    "businessDomain": "cross_summary",  
    "lifeCycleStatus": "Active_To_Active",
    "Scope": "All categories"
}}
If the question does not match any of the two domains, respond with:
{{
    "error": "Unrecognized question format."
}}
"""
        formatted_prompt = prompt.format(user_question=chat_text)

        print("Chatgpt Prompt:", formatted_prompt)

        # Process chat text using the service
        result = process_chat_text(formatted_prompt)
        print("Chatgpt Result:", result)

        # Extract the value of the answer from the result
        response = extract_json_response(result['response'])

        # Ensure response is a valid JSON object
        return Response(response, mimetype='application/json')
