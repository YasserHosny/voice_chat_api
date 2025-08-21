#!/usr/bin/env python3
"""
Test script to validate Bedrock Bearer Token configuration
"""

import os
from config import config
from app.repositories.bedrock_repository import get_bedrock_nova_pro_response2

def test_bearer_token_config():
    """Test if bearer token is configured"""
    print("🔍 Testing Bedrock Bearer Token Configuration...")
    print(f"   AWS_DEFAULT_REGION: {config.AWS_DEFAULT_REGION}")
    print(f"   AWS_BEARER_TOKEN_BEDROCK: {'✅ Set' if config.AWS_BEARER_TOKEN_BEDROCK else '❌ Not Set'}")
    
    if not config.AWS_BEARER_TOKEN_BEDROCK:
        print("\n❌ ERROR: AWS_BEARER_TOKEN_BEDROCK is not configured!")
        print("   Please set the environment variable:")
        print("   set AWS_BEARER_TOKEN_BEDROCK=your_bearer_token_here")
        return False
    
    print("✅ Bearer token configuration looks good!")
    return True

def test_bedrock_request():
    """Test a simple Bedrock request"""
    if not test_bearer_token_config():
        return
    
    print("\n🚀 Testing Bedrock API call...")
    
    try:
        test_prompt = "Hello, this is a test. Please respond with 'Bedrock is working!'"
        response = get_bedrock_nova_pro_response2(test_prompt)
        
        if response:
            print("✅ SUCCESS: Bedrock API call completed!")
            print(f"   Response: {response}")
        else:
            print("❌ FAILED: No response received from Bedrock")
            
    except Exception as e:
        print(f"❌ ERROR: Bedrock API call failed: {e}")

if __name__ == "__main__":
    test_bedrock_request()
