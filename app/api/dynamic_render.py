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

Ignore any previous conversation, then classify it into one of the following business domains and extract the relevant parameters:

---

1. **Product Portfolio**: The user is asking about a product portfolio query.
   - **Business Functions:**
     - **Total Parts**: If the user asks for the total number of parts.
     - **Product Categories**: If the user asks for product categories.
       - **Scope**: Extract if the user requests "Top 10" or "All" categories.
     - **Lifecycle**: If the user asks about product lifecycle statistics.
     - **RoHS**: If the user asks about RoHS compliance.

2. **Obsolescence**: The user is asking about product obsolescence trends or statistics.
   - **Business Functions:**
     - **Time Trend**: If the user asks for monthly obsolescence trends.
     - **Statistics**: If the user asks for obsolescence statistics.

3. **Cross Summary**: The user is asking about cross-analysis comparisons.
   - **Business Functions:**
     - **Product Categories**: If the user asks about competitive analysis in product categories.
       - **Scope**: Extract if the user requests "Top 10" or "All" categories.
     - **Relations by Competitor**: If the user asks about competitor cross-references.

4. **Market Performance**: The user is asking about market performance metrics.
   - **Business Functions:**
     - **Best Competitive Performance**: If the user asks about the best-performing competitors.
     - **Price Comparison**: If the user asks about price differences across suppliers.
     - **Lead Time**: If the user asks about supplier lead times.
     - **Inventory Comparison**: If the user asks about supplier inventory levels.

---

Return the result **ONLY** in the following JSON format without additional explanations:

**Example 1:**
```json
{{
    "businessDomain": {{
        "name": "product_portfolio",
        "businessFunction": {{
            "name": "product_categories",
            "Scope": "Top 10"
        }}
    }},
    "chartConfig": {{
        "chartType": "bar",
        "chartGap": 3,
        "chartSpacing": 0.5,
        "showLegend": false,
        "showTooltip": true,
        "chartStyle": {{
            "height": "400px",
            "width": "100%"
        }}
    }}
}}
```

**Example 2:**
```json
{{
    "businessDomain": {{
        "name": "obsolescence",
        "businessFunction": {{
            "name": "time_trend"
        }}
    }},
    "chartConfig": {{
        "chartType": "line",
        "chartGap": 2,
        "chartSpacing": 0.7,
        "showLegend": true,
        "showTooltip": true,
        "chartStyle": {{
            "height": "500px",
            "width": "100%"
        }}
    }}
}}
```

**Example 3:**
```json
{{
    "businessDomain": {{
        "name": "cross_summary",
        "businessFunction": {{
            "name": "relations_by_competitor"
        }}
    }},
    "chartConfig": {{
        "chartType": "bar",
        "chartGap": 3,
        "chartSpacing": 0.5,
        "showLegend": false,
        "showTooltip": true,
        "chartStyle": {{
            "height": "400px",
            "width": "100%"
        }}
    }}
}}
```

**Example 4:**
```json
{{
    "businessDomain": {{
        "name": "market_performance",
        "businessFunction": {{
            "name": "price"
        }}
    }},
    "chartConfig": {{
        "chartType": "line",
        "chartGap": 2,
        "chartSpacing": 0.7,
        "showLegend": true,
        "showTooltip": true,
        "chartStyle": {{
            "height": "500px",
            "width": "100%"
        }}
    }}
}}

If the question does not match any of the categories, respond with:
```json
{{
    "error": "Unrecognized question format."
}}
```
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
