import httpx
from .vulnerability_models import VulnerabilityFinding
from ..utils.config import CONFIDENCE_HIGH, CONFIDENCE_MEDIUM, CONFIDENCE_LOW, RISK_HIGH, RISK_MEDIUM

class ResponseAnalyzer:
    def analyze_upload_response(self, response: httpx.Response, filename: str) -> dict:
        """
        Analyzes the upload response to guess if upload was successful and where.
        """
        result = {
            "success_probability": 0,
            "path_leaked": None,
            "status_code": response.status_code,
            "length": len(response.content)
        }

        # 1. Status Code Check
        if 200 <= response.status_code < 300:
            result["success_probability"] += 30
        elif response.status_code == 403 or response.status_code == 401:
            result["success_probability"] -= 50 # likely blocked/auth required
        elif response.status_code == 500:
             # Sometimes 500 means "I crashed trying to process your shell", which is interesting
             pass

        # 2. Reflected Filename
        if filename in response.text:
            result["success_probability"] += 40
            # Try to extract path context? (simplified)
            
        # 3. Common success keywords
        success_keywords = ["uploaded", "success", "completed", "saved"]
        if any(keyword in response.text.lower() for keyword in success_keywords):
             result["success_probability"] += 30

        return result

    def analyze_execution_response(self, response: httpx.Response, expected_output: str) -> bool:
        """
        Checks if the payload executed (e.g., matching calculation result).
        """
        if response.status_code == 200:
            if expected_output in response.text:
                return True
        return False
