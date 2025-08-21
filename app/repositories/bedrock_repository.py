from config import config
import requests
import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
import json


# Create a Bedrock client with bearer token authentication
# Note: Bearer token authentication requires direct HTTP requests
# Standard boto3 client won't work with bearer tokens
region = config.AWS_DEFAULT_REGION
bedrock_endpoint = f"https://bedrock-runtime.{region}.amazonaws.com"


def get_bedrock_response_with_bearer_token(prompt, model_id="amazon.titan-embed-text-v2:0"):
    """Get response from Bedrock using Bearer Token authentication"""
    print("[INFO] Sending request to Amazon Bedrock with Bearer Token:", prompt)

    if not config.AWS_BEARER_TOKEN_BEDROCK:
        raise ValueError("AWS_BEARER_TOKEN_BEDROCK is not configured")

    url = f"{bedrock_endpoint}/model/{model_id}/invoke"

    body = {
        "inputText": prompt,
        "dimensions": 512,
        "normalize": True
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {config.AWS_BEARER_TOKEN_BEDROCK}"
    }

    try:
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()

        response_data = response.json()
        print(
            "[INFO] Bedrock response received successfully, repsonse_data: ", response_data)

        # Extract the embedding from the response
        embedding = response_data.get('embedding', [])
        print("[DEBUG] Embedding:", embedding[:10]
              if embedding else "No embedding found")

        return embedding
    except Exception as e:
        print(f"[ERROR] Bedrock request failed: {e}")
        raise


def get_bedrock_nova_pro_response(prompt, model_id="amazon.nova-pro-v1:0"):
    """Get response from Bedrock Nova Pro using Bearer Token authentication"""
    print("[INFO] Sending request to Amazon Bedrock Nova Pro with Bearer Token:", prompt)

    if not config.AWS_BEARER_TOKEN_BEDROCK:
        raise ValueError("AWS_BEARER_TOKEN_BEDROCK is not configured")

    url = f"{bedrock_endpoint}/model/{model_id}/invoke"

    body = {
        "inferenceConfig": {
            "max_new_tokens": 1000
        },
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {config.AWS_BEARER_TOKEN_BEDROCK}"
    }

    try:
        response = requests.post(url, json=body, headers=headers)
        response.raise_for_status()

        response_data = response.json()
        print("[INFO] Bedrock Nova Pro response received successfully")

        # Extract the completion from the response
        output = response_data.get("completion", "").strip()
        if not output and 'output' in response_data:
            output = response_data['output'].get('message', {}).get(
                'content', [{}])[0].get('text', '')

        print("[DEBUG] Received Bedrock response:", output)
        return output
    except Exception as e:
        print(f"[ERROR] Bedrock Nova Pro request failed: {e}")
        raise


def get_bedrock_nova_pro_response2(prompt, model_id="amazon.nova-pro-v1:0"):
    """Get response from Bedrock using Bearer Token authentication for LLM models"""
    print("[INFO] Starting get_bedrock_nova_pro_response2 with Bearer Token")

    if not config.AWS_BEARER_TOKEN_BEDROCK:
        raise ValueError("AWS_BEARER_TOKEN_BEDROCK is not configured")

    url = f"{bedrock_endpoint}/model/{model_id}/invoke"

    payload = {
        "inferenceConfig": {"max_new_tokens": 1000},
        "messages": [
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ]
    }
    print("[DEBUG] Payload:", payload)
    print("[DEBUG] URL:", url)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {config.AWS_BEARER_TOKEN_BEDROCK}"
    }
    print("[DEBUG] AWS_BEARER_TOKEN_BEDROCK: ",
          config.AWS_BEARER_TOKEN_BEDROCK)

    try:
        response = requests.post(url, json=payload, headers=headers)
        print("[INFO] Received response with status code:", response.status_code)

        if response.status_code != 200:
            print(
                f"[ERROR] Request failed with status {response.status_code}: {response.text}")
            return None

        result = response.json()
        print("[INFO] Bedrock response parsed successfully")
        print("[DEBUG] Bedrock response:", result)

        # Extract the content from the response
        if 'output' in result and 'message' in result['output']:
            content = result['output']['message']['content'][0]['text']
            return content
        elif 'content' in result:
            return result['content']
        else:
            return result

    except Exception as e:
        print(f"[ERROR] Bedrock request failed: {e}")
        return None


def get_bedrock_response(prompt, model_id="amazon.nova-pro-v1:0", region="us-east-1"):
    """Get response from Amazon Bedrock using temporary AWS credentials"""
    print("[INFO] Starting get_bedrock_response using temporary credentials")

    # Load credentials (these could be from env vars, or a boto3 profile)
    session = boto3.Session()
    creds = session.get_credentials().get_frozen_credentials()

    endpoint = f"https://bedrock-runtime.{region}.amazonaws.com"
    url = f"{endpoint}/model/{model_id}/invoke"

    payload = {
        "inferenceConfig": {"max_new_tokens": 1000},
        "messages": [{"role": "user", "content": [{"text": prompt}]}]
    }

    # Create AWSRequest
    request = AWSRequest(
        method="POST",
        url=url,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )

    # Sign the request using SigV4
    SigV4Auth(creds, "bedrock", region).add_auth(request)

    # Send the request
    response = requests.post(
        url,
        data=request.body,
        headers=dict(request.headers)
    )

    print("[INFO] Received response:", response.status_code)
    if response.status_code != 200:
        print("[ERROR] Bedrock error:", response.text)
        return None

    result = response.json()
    print("[DEBUG] Response JSON:", result)

    # Extract content
    if 'output' in result and 'message' in result['output']:
        return result['output']['message']['content'][0]['text']
    elif 'content' in result:
        return result['content']
    return result
