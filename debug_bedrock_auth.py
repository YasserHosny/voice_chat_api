#!/usr/bin/env python3
"""
Debug script to test different Bedrock authentication methods
"""

import requests
import json
from config import config

def test_bearer_token_formats():
    """Test different bearer token formats"""
    
    print("🔍 Testing Bedrock Authentication...")
    print(f"   Region: {config.AWS_DEFAULT_REGION}")
    print(f"   Token length: {len(config.AWS_BEARER_TOKEN_BEDROCK) if config.AWS_BEARER_TOKEN_BEDROCK else 0}")
    
    # Test different model IDs
    test_models = [
        "meta.llama3-2-1b-instruct-v1:0",
        "meta.llama3-2-3b-instruct-v1:0", 
        "amazon.nova-micro-v1:0",
        "amazon.nova-lite-v1:0",
        "anthropic.claude-3-haiku-20240307-v1:0"
    ]
    
    for model_id in test_models:
        print(f"\n🧪 Testing model: {model_id}")
        test_model_request(model_id)

def test_model_request(model_id):
    """Test a specific model with different auth formats"""
    
    url = f"https://bedrock-runtime.{config.AWS_DEFAULT_REGION}.amazonaws.com/model/{model_id}/invoke"
    
    payload = {
        "inferenceConfig": {"max_new_tokens": 10},
        "messages": [
            {
                "role": "user",
                "content": [{"text": "Hello"}]
            }
        ]
    }
    
    # Test different authorization header formats
    auth_formats = [
        f"Bearer {config.AWS_BEARER_TOKEN_BEDROCK}",
        f"{config.AWS_BEARER_TOKEN_BEDROCK}",
        f"AWS4-HMAC-SHA256 {config.AWS_BEARER_TOKEN_BEDROCK}"
    ]
    
    for i, auth_header in enumerate(auth_formats, 1):
        print(f"   Format {i}: {auth_header[:50]}...")
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": auth_header
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ SUCCESS!")
                result = response.json()
                print(f"   Response: {json.dumps(result, indent=2)[:200]}...")
                return True
            else:
                print(f"   ❌ Error: {response.text[:100]}...")
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)[:100]}...")
    
    return False

def list_available_models():
    """Try to list available models"""
    print("\n📋 Attempting to list available models...")
    
    # Try different endpoints
    endpoints = [
        f"https://bedrock.{config.AWS_DEFAULT_REGION}.amazonaws.com/foundation-models",
        f"https://bedrock-runtime.{config.AWS_DEFAULT_REGION}.amazonaws.com/foundation-models"
    ]
    
    for endpoint in endpoints:
        print(f"   Trying: {endpoint}")
        
        headers = {
            "Authorization": f"Bearer {config.AWS_BEARER_TOKEN_BEDROCK}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                models = response.json()
                print(f"   Found {len(models.get('modelSummaries', []))} models")
                for model in models.get('modelSummaries', [])[:5]:
                    print(f"     - {model.get('modelId', 'Unknown')}")
                return
            else:
                print(f"   Error: {response.text[:100]}...")
                
        except Exception as e:
            print(f"   Exception: {str(e)[:100]}...")

if __name__ == "__main__":
    if not config.AWS_BEARER_TOKEN_BEDROCK:
        print("❌ AWS_BEARER_TOKEN_BEDROCK is not configured!")
        exit(1)
    
    list_available_models()
    test_bearer_token_formats()
