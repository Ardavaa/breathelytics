#!/usr/bin/env python3
"""
Test script for LLM integration with Breathelytics backend

This script tests the Gemini LLM integration by simulating ML prediction results
and generating AI insights.
"""

import os
import sys
import json
import logging
from datetime import datetime

# Add the backend directory to path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm_service import generate_medical_insights
from config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_llm_integration():
    """Test the LLM integration with sample prediction data."""
    
    # Sample ML prediction results for different conditions
    test_cases = [
        {
            "name": "High Confidence Pneumonia",
            "prediction_result": {
                "prediction": "Pneumonia",
                "prediction_code": 6,
                "probability": 0.82,
                "all_probabilities": {
                    "Asthma": 0.05,
                    "Bronchiectasis": 0.03,
                    "Bronchiolitis": 0.02,
                    "COPD": 0.05,
                    "Healthy": 0.04,
                    "LRTI": 0.04,
                    "Pneumonia": 0.82,
                    "URTI": 0.01
                },
                "processing_time_seconds": 2.45,
                "feature_count": 112
            }
        },
        {
            "name": "Moderate Confidence Asthma",
            "prediction_result": {
                "prediction": "Asthma",
                "prediction_code": 0,
                "probability": 0.65,
                "all_probabilities": {
                    "Asthma": 0.65,
                    "Bronchiectasis": 0.08,
                    "Bronchiolitis": 0.05,
                    "COPD": 0.12,
                    "Healthy": 0.06,
                    "LRTI": 0.02,
                    "Pneumonia": 0.01,
                    "URTI": 0.01
                },
                "processing_time_seconds": 1.89,
                "feature_count": 112
            }
        },
        {
            "name": "Healthy Result",
            "prediction_result": {
                "prediction": "Healthy",
                "prediction_code": 4,
                "probability": 0.89,
                "all_probabilities": {
                    "Asthma": 0.02,
                    "Bronchiectasis": 0.01,
                    "Bronchiolitis": 0.01,
                    "COPD": 0.02,
                    "Healthy": 0.89,
                    "LRTI": 0.02,
                    "Pneumonia": 0.01,
                    "URTI": 0.02
                },
                "processing_time_seconds": 1.67,
                "feature_count": 112
            }
        }
    ]
    
    # Check if API key is available
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        logger.warning("GEMINI_API_KEY not found. Set environment variable or check config.")
        return
    
    logger.info(f"Testing LLM integration with API key: {api_key[:10]}...")
    
    # Test each case
    for i, test_case in enumerate(test_cases, 1):
        logger.info(f"\n{'='*60}")
        logger.info(f"Test Case {i}: {test_case['name']}")
        logger.info(f"{'='*60}")
        
        try:
            # Generate insights
            start_time = datetime.now()
            insights = generate_medical_insights(test_case['prediction_result'])
            end_time = datetime.now()
            
            processing_time = (end_time - start_time).total_seconds()
            
            if insights:
                logger.info(f"✅ LLM insights generated successfully in {processing_time:.2f}s")
                logger.info(f"LLM Status: {insights.get('llm_status', 'unknown')}")
                
                # Display key information
                print("\n📋 GENERATED INSIGHTS:")
                print(f"Summary: {insights.get('summary', 'N/A')}")
                print(f"Risk Level: {insights.get('risk_level', 'N/A')}")
                print(f"Condition: {insights.get('condition_explanation', 'N/A')}")
                
                if 'recommendations' in insights:
                    print("\n💡 RECOMMENDATIONS:")
                    rec = insights['recommendations']
                    for category, items in rec.items():
                        print(f"  {category.title()}: {', '.join(items[:2])}...")
                
                # Check for errors
                if 'error_message' in insights:
                    logger.warning(f"⚠️  Error occurred: {insights['error_message']}")
                
                print(f"\n🔧 Processing Time: {insights.get('processing_time_ms', 0)}ms")
                
            else:
                logger.error("❌ No insights generated")
                
        except Exception as e:
            logger.error(f"❌ Test failed: {str(e)}")
        
        print("\n")
    
    logger.info("LLM integration testing completed!")


def test_api_connectivity():
    """Test basic connectivity to Gemini API."""
    
    logger.info("Testing Gemini API connectivity...")
    
    try:
        from llm_service import GeminiLLMService
        
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            logger.error("❌ GEMINI_API_KEY not found")
            return False
        
        # Create service instance
        service = GeminiLLMService(api_key)
        
        # Test with simple prediction
        test_prediction = {
            "prediction": "Healthy",
            "probability": 0.95,
            "all_probabilities": {
                "Healthy": 0.95,
                "Asthma": 0.02,
                "Pneumonia": 0.01,
                "COPD": 0.01,
                "LRTI": 0.01,
                "URTI": 0.00,
                "Bronchiectasis": 0.00,
                "Bronchiolitis": 0.00
            }
        }
        
        # Generate insights
        insights = service.generate_insights(test_prediction)
        
        if insights and insights.get('llm_status') == 'success':
            logger.info("✅ Gemini API connectivity test PASSED")
            return True
        else:
            logger.warning(f"⚠️  API test returned fallback: {insights.get('llm_status', 'unknown')}")
            return False
            
    except Exception as e:
        logger.error(f"❌ API connectivity test FAILED: {str(e)}")
        return False


def main():
    """Main test function."""
    
    print("🧪 BREATHELYTICS LLM INTEGRATION TEST")
    print("=" * 50)
    
    # Test 1: API Connectivity
    print("\n1️⃣  Testing API Connectivity...")
    api_test_passed = test_api_connectivity()
    
    # Test 2: LLM Integration
    print("\n2️⃣  Testing LLM Integration...")
    test_llm_integration()
    
    # Summary
    print("\n📊 TEST SUMMARY")
    print("-" * 30)
    print(f"API Connectivity: {'✅ PASS' if api_test_passed else '❌ FAIL'}")
    print("LLM Integration: ✅ COMPLETED (check logs for details)")
    
    if not api_test_passed:
        print("\n⚠️  TROUBLESHOOTING:")
        print("1. Check if GEMINI_API_KEY is set correctly")
        print("2. Verify internet connection")
        print("3. Check if API key has proper permissions")
        print("4. Review the logs above for specific error messages")


if __name__ == "__main__":
    main() 