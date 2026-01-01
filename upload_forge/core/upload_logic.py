from typing import Optional, Tuple
from .request_engine import RequestEngine
from .response_analyzer import ResponseAnalyzer
from .vulnerability_models import VulnerabilityFinding
from ..utils.logger import logger
from ..utils.config import *
import random

class UploadLogic:
    def __init__(self, engine: RequestEngine, analyzer: ResponseAnalyzer):
        self.engine = engine
        self.analyzer = analyzer

    async def test_payload(self, 
                           target_url: str, 
                           file_param: str, 
                           payload: dict,
                           upload_dir: Optional[str] = None) -> Optional[VulnerabilityFinding]:
        
        # 1. Prepare Payload
        content = payload['content']
        content_type = "application/octet-stream"
        
        # Handle filename: use provided or generate one
        if payload.get('filename'):
            actual_filename = payload['filename']
        else:
            # Randomize to avoid collisions/caching
            rand_suffix = str(random.randint(1000, 9999))
            actual_filename = f"test_{rand_suffix}.{payload['ext']}"
            
        # 2. Upload
        try:
            response = await self.engine.upload_file(
                url=target_url,
                file_field_name=file_param,
                filename=actual_filename,
                file_content=content,
                content_type=content_type
            )
        except Exception as e:
            logger.warning(f"Upload failed for {payload['type']}: {e}")
            return None

        # 3. Analyze Upload Response
        analysis = self.analyzer.analyze_upload_response(response, actual_filename)
        
        # 4. Verification (Attempt to access the file)
        verified_execution = False
        verified_upload = False
        verification_url = None
        
        # Strategy A: Use provided upload_dir
        if upload_dir:
            # Ensure correct slash handling
            base = upload_dir.rstrip("/")
            
            # For double extensions or null bytes, we need to know how the server saves it.
            check_filename = actual_filename
            if "%00" in actual_filename:
                check_filename = actual_filename.split("%00")[0]
            
            verification_url = f"{base}/{check_filename}"
            
            try:
                # logger.debug(f"Verifying at: {verification_url}")
                check_resp = await self.engine.check_file_existence(verification_url)
                # logger.debug(f"Verification status: {check_resp.status_code}, Length: {len(check_resp.content)}")
                
                if check_resp.status_code == 200:
                    verified_upload = True
                    
                    # Check for execution evidence (RCE)
                    if "UploadForge_Test_Success_" in str(content):
                        if self.analyzer.analyze_execution_response(check_resp, "46"): # 23 * 2
                            verified_execution = True
                            # logger.debug("RCE Verified via calculation")
                    elif "UploadForge" in str(content):
                        if self.analyzer.analyze_execution_response(check_resp, "UploadForge"):
                             # Simple echo might be just source code disclosure if no calculation
                             pass
                    
                    # Special check: If content is exactly the same, but no RCE, it's Arbitrary File Upload
                    if check_resp.content == content:
                        verified_upload = True # Confirmed stored
                        # logger.debug("Content match confirmed")
                        
            except Exception as e:
                logger.debug(f"Verification check failed: {e}")

        # 5. Construct Finding
        if verified_execution:
            return VulnerabilityFinding(
                name=f"Remote Code Execution ({payload['type']})",
                description=f"Successfully uploaded and executed a {payload['type']} file.",
                risk_level=RISK_CRITICAL,
                confidence=CONFIDENCE_CERTAIN,
                url=target_url,
                payload=actual_filename,
                proof=f"File accessible at {verification_url} and executed code.",
                remediation="Validate file extensions against a whitelist, disable execution in upload directory.",
                request_data=str(response.request.headers),
                response_data=response.text[:500]
            )
        
        if verified_upload:
             return VulnerabilityFinding(
                name=f"Arbitrary File Upload ({payload['type']})",
                description=f"Successfully uploaded a {payload['type']} file. Server does not block this extension.",
                risk_level=RISK_HIGH,
                confidence=CONFIDENCE_CERTAIN,
                url=target_url,
                payload=actual_filename,
                proof=f"File found at {verification_url}",
                remediation="Validate file extensions against a whitelist.",
                request_data=str(response.request.headers),
                response_data=response.text[:500]
            )
        
        # If not verified but high probability (e.g. 200 OK and filename reflected)
        if analysis['success_probability'] > 70:
             return VulnerabilityFinding(
                name=f"Potential File Upload ({payload['type']})",
                description=f"Upload request appeared successful but file location could not be verified.",
                risk_level=RISK_MEDIUM,
                confidence=CONFIDENCE_MEDIUM,
                url=target_url,
                payload=actual_filename,
                proof=f"Server responded with {response.status_code} and success indicators.",
                remediation="Ensure files are not stored in web root.",
                 request_data=str(response.request.headers),
                response_data=response.text[:500]
            )

        return None
