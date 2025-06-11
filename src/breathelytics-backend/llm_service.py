"""
Google Gemini LLM Service for Breathelytics Medical Insights

Integrates with Google Gemini API to provide AI-powered medical interpretations
of respiratory disease predictions from the ML model.
"""

import os
import json
import logging
import requests
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger('breathelytics')


class GeminiLLMService:
    """Service class for Google Gemini LLM integration."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        """
        Initialize Gemini LLM service.
        
        Args:
            api_key: Google AI API key
            model_name: Gemini model name to use
        """
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.timeout = 30
        self.max_retries = 3
        
        # Disease information mapping
        self.disease_info = {
            "Asthma": {
                "description": "condition where airways narrow and swell, producing extra mucus",
                "severity": "Moderate",
                "urgency": "moderate"
            },
            "Bronchiectasis": {
                "description": "condition where bronchi are abnormally widened and thickened",
                "severity": "Severe", 
                "urgency": "high"
            },
            "Bronchiolitis": {
                "description": "inflammation of the small airways in the lungs",
                "severity": "Mild to Moderate",
                "urgency": "moderate"
            },
            "COPD": {
                "description": "chronic obstructive pulmonary disease that is progressive",
                "severity": "Severe",
                "urgency": "high"
            },
            "Healthy": {
                "description": "normal respiratory function with no detected abnormalities",
                "severity": "Normal",
                "urgency": "low"
            },
            "LRTI": {
                "description": "lower respiratory tract infection affecting lungs and airways",
                "severity": "Moderate",
                "urgency": "moderate"
            },
            "Pneumonia": {
                "description": "infection that inflames air sacs in one or both lungs",
                "severity": "Severe",
                "urgency": "high"
            },
            "URTI": {
                "description": "upper respiratory tract infection affecting nose, throat, and sinuses",
                "severity": "Mild",
                "urgency": "low"
            }
        }
    
    def _build_prompt(self, prediction_result: Dict[str, Any]) -> str:
        """
        Build the prompt for Gemini based on ML prediction results.
        
        Args:
            prediction_result: ML prediction output
            
        Returns:
            str: Formatted prompt for Gemini
        """
        prediction = prediction_result['prediction']
        probability = prediction_result['probability']
        all_probs = prediction_result['all_probabilities']
        
        # Build probability distribution text
        prob_lines = []
        for condition, prob in sorted(all_probs.items(), key=lambda x: x[1], reverse=True):
            prob_lines.append(f"- {condition}: {prob:.0%}")
        
        prob_text = "\n".join(prob_lines)
        
        prompt = f"""As a professional AI Medical Assistant, analyze the following prediction results:

The patient shows a high likelihood of having {prediction} ({probability:.0%}). Here are the other potential conditions based on the patient's respiratory sounds:

{prob_text}

Provide professional diagnostic insights that are easy to understand for laypeople. Briefly explain what {prediction} is, why it's likely occurring, and suggest follow-up actions such as doctor visits, additional tests, or initial home care.

Provide your response in valid JSON format with the following structure:
{{
    "summary": "Easy-to-understand summary of results",
    "condition_explanation": "Explanation of {prediction} condition in layman's terms",
    "confidence_interpretation": "Interpretation of {probability:.0%} confidence level",
    "insights": [
        "Key insight based on probabilities",
        "Analysis of respiratory sound patterns",
        "Factors that may influence results"
    ],
    "recommendations": {{
        "immediate": ["Immediate actions to take"],
        "monitoring": ["Symptoms to watch for"],
        "lifestyle": ["Lifestyle recommendations"],
        "medical": ["When to see a doctor"]
    }},
    "risk_level": "LOW/MODERATE/HIGH",
    "next_steps": "Recommended next steps",
    "disclaimer": "Warning that this is not a definitive medical diagnosis"
}}

IMPORTANT: 
- Use clear, easy-to-understand English
- Do not make definitive diagnoses
- Always recommend medical consultation for concerning results
- Provide reassuring yet accurate information
- Ensure output is valid JSON"""

        return prompt
    
    def _call_gemini_api(self, prompt: str) -> Dict[str, Any]:
        """
        Make API call to Google Gemini.
        
        Args:
            prompt: The prompt to send to Gemini
            
        Returns:
            Dict: Gemini API response
            
        Raises:
            Exception: If API call fails
        """
        url = f"{self.base_url}/{self.model_name}:generateContent"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.1,  # Low temperature for medical accuracy
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 2048,
            }
        }
        
        # Add API key to URL
        url_with_key = f"{url}?key={self.api_key}"
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Calling Gemini API (attempt {attempt + 1})")
                response = requests.post(
                    url_with_key,
                    headers=headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"Gemini API returned status {response.status_code}: {response.text}")
                    if attempt == self.max_retries - 1:
                        raise Exception(f"Gemini API failed with status {response.status_code}")
                    
            except requests.exceptions.Timeout:
                logger.warning(f"Gemini API timeout (attempt {attempt + 1})")
                if attempt == self.max_retries - 1:
                    raise Exception("Gemini API timeout after multiple attempts")
                    
            except Exception as e:
                logger.error(f"Gemini API error (attempt {attempt + 1}): {str(e)}")
                if attempt == self.max_retries - 1:
                    raise Exception(f"Gemini API failed: {str(e)}")
        
        raise Exception("Gemini API failed after all retries")
    
    def _parse_gemini_response(self, gemini_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse and validate Gemini API response.
        
        Args:
            gemini_response: Raw response from Gemini API
            
        Returns:
            Dict: Parsed insights
        """
        try:
            # Extract text from Gemini response
            candidates = gemini_response.get('candidates', [])
            if not candidates:
                raise ValueError("No candidates in Gemini response")
            
            content = candidates[0].get('content', {})
            parts = content.get('parts', [])
            if not parts:
                raise ValueError("No parts in Gemini response")
            
            text_response = parts[0].get('text', '')
            if not text_response:
                raise ValueError("No text in Gemini response")
            
            logger.debug(f"Raw Gemini response: {text_response}")
            
            # Try to extract JSON from response
            # Sometimes Gemini wraps JSON in markdown code blocks
            text_response = text_response.strip()
            if text_response.startswith('```json'):
                text_response = text_response[7:]
            if text_response.endswith('```'):
                text_response = text_response[:-3]
            if text_response.startswith('```'):
                text_response = text_response[3:]
            
            text_response = text_response.strip()
            
            # Parse JSON
            parsed_insights = json.loads(text_response)
            
            # Validate required fields
            required_fields = ['summary', 'condition_explanation', 'insights', 'recommendations']
            for field in required_fields:
                if field not in parsed_insights:
                    logger.warning(f"Missing required field: {field}")
                    parsed_insights[field] = f"{field.replace('_', ' ').title()} information not available"
            
            # Ensure recommendations has required subfields
            if 'recommendations' in parsed_insights:
                rec = parsed_insights['recommendations']
                for subfield in ['immediate', 'monitoring', 'lifestyle', 'medical']:
                    if subfield not in rec:
                        rec[subfield] = [f"Consult with medical professionals for {subfield} guidance"]
            
            logger.info("Successfully parsed Gemini response")
            return parsed_insights
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Gemini: {str(e)}")
            logger.debug(f"Problematic text: {text_response}")
            raise ValueError(f"Invalid JSON response from Gemini: {str(e)}")
            
        except Exception as e:
            logger.error(f"Error parsing Gemini response: {str(e)}")
            raise ValueError(f"Failed to parse Gemini response: {str(e)}")
    
    def _generate_fallback_insights(self, prediction_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate fallback insights when Gemini API fails.
        
        Args:
            prediction_result: ML prediction output
            
        Returns:
            Dict: Fallback insights
        """
        prediction = prediction_result['prediction']
        probability = prediction_result['probability']
        
        disease_details = self.disease_info.get(prediction, {
            "description": "respiratory condition detected by the system",
            "severity": "Requires evaluation",
            "urgency": "moderate"
        })
        
        # Determine risk level based on prediction and confidence
        if prediction == "Healthy":
            risk_level = "LOW"
        elif probability > 0.7 and disease_details["urgency"] == "high":
            risk_level = "HIGH"
        elif probability > 0.5:
            risk_level = "MODERATE"
        else:
            risk_level = "LOW"
        
        return {
            "summary": f"Analysis indicates possible {prediction} with {probability:.0%} confidence level",
            "condition_explanation": f"{prediction} is {disease_details['description']}",
            "confidence_interpretation": f"Confidence level of {probability:.0%} indicates {'strong indication' if probability > 0.7 else 'moderate possibility' if probability > 0.5 else 'weak indication'}",
            "insights": [
                f"System detected sound patterns consistent with {prediction}",
                f"Confidence level of {probability:.0%} based on audio feature analysis",
                "This result serves as initial screening, not a definitive medical diagnosis"
            ],
            "recommendations": {
                "immediate": [
                    "Consult with a doctor for further evaluation",
                    "Document any symptoms you are currently experiencing"
                ],
                "monitoring": [
                    "Watch for changes in breathing patterns",
                    "Monitor symptoms such as shortness of breath or coughing"
                ],
                "lifestyle": [
                    "Avoid cigarette smoke and air pollutants",
                    "Maintain good hand hygiene and clean environment"
                ],
                "medical": [
                    "See a doctor immediately if symptoms worsen",
                    "Undergo routine examinations as recommended by medical professionals"
                ]
            },
            "risk_level": risk_level,
            "next_steps": "Consult with medical professionals for accurate diagnosis",
            "disclaimer": "This result is an initial screening using AI. Medical consultation is still required for proper diagnosis and treatment.",
            "llm_status": "fallback_used"
        }
    
    def generate_insights(self, prediction_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate medical insights from ML prediction results using Gemini.
        
        Args:
            prediction_result: ML prediction output containing prediction, probability, etc.
            
        Returns:
            Dict: Medical insights and recommendations
        """
        start_time = datetime.now()
        
        try:
            # Validate input
            required_fields = ['prediction', 'probability', 'all_probabilities']
            for field in required_fields:
                if field not in prediction_result:
                    raise ValueError(f"Missing required field: {field}")
            
            # Build prompt
            prompt = self._build_prompt(prediction_result)
            logger.info(f"Generated prompt for condition: {prediction_result['prediction']}")
            
            # Call Gemini API
            gemini_response = self._call_gemini_api(prompt)
            
            # Parse response
            insights = self._parse_gemini_response(gemini_response)
            
            # Add metadata
            insights['llm_status'] = 'success'
            insights['processing_time_ms'] = int((datetime.now() - start_time).total_seconds() * 1000)
            
            logger.info(f"Generated insights successfully for {prediction_result['prediction']}")
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate insights with Gemini: {str(e)}")
            
            # Return fallback insights
            fallback_insights = self._generate_fallback_insights(prediction_result)
            fallback_insights['processing_time_ms'] = int((datetime.now() - start_time).total_seconds() * 1000)
            fallback_insights['error_message'] = str(e)
            
            logger.info(f"Returned fallback insights for {prediction_result['prediction']}")
            return fallback_insights


# Global instance
_llm_service: Optional[GeminiLLMService] = None


def get_llm_service() -> Optional[GeminiLLMService]:
    """Get or create the global LLM service instance."""
    global _llm_service
    
    if _llm_service is None:
        api_key = os.environ.get('GEMINI_API_KEY')
        if api_key:
            try:
                _llm_service = GeminiLLMService(api_key)
                logger.info("LLM service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize LLM service: {str(e)}")
        else:
            logger.warning("GEMINI_API_KEY not found in environment variables")
    
    return _llm_service


def generate_medical_insights(prediction_result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Generate medical insights from prediction results.
    
    Args:
        prediction_result: ML prediction output
        
    Returns:
        Dict with insights or None if LLM service unavailable
    """
    llm_service = get_llm_service()
    
    if llm_service is None:
        logger.warning("LLM service not available, skipping insights generation")
        return None
    
    try:
        return llm_service.generate_insights(prediction_result)
    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}")
        return None 