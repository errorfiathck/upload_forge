import httpx
from typing import Dict, Optional, Any
from ..utils.logger import logger
from ..utils.config import DEFAULT_TIMEOUT, DEFAULT_USER_AGENT

from .vulnerability_models import TrafficLog
from datetime import datetime

class RequestEngine:
    def __init__(self, 
                 proxies: Optional[Dict] = None, 
                 headers: Optional[Dict] = None, 
                 cookies: Optional[Dict] = None,
                 timeout: int = DEFAULT_TIMEOUT):
        
        self.proxies = proxies
        self.headers = headers or {}
        self.cookies = cookies or {}
        self.timeout = timeout
        self.log_callback = None
        self.request_counter = 0
        
        # Ensure User-Agent is set
        if "User-Agent" not in self.headers:
            self.headers["User-Agent"] = DEFAULT_USER_AGENT

        self.client = httpx.AsyncClient(
            proxies=self.proxies,
            headers=self.headers,
            cookies=self.cookies,
            timeout=self.timeout,
            verify=False, # Often needed for pentesting targets with self-signed certs
            trust_env=False # Ignore system proxies to avoid issues with localhost
        )

    def set_log_callback(self, callback):
        self.log_callback = callback

    def _log_traffic(self, response: httpx.Response):
        if self.log_callback:
            self.request_counter += 1
            
            # Format headers
            req_headers = "\n".join([f"{k}: {v}" for k, v in response.request.headers.items()])
            res_headers = "\n".join([f"{k}: {v}" for k, v in response.headers.items()])
            
            # Handle bodies (truncate if too large for memory safety in GUI, but user asked for full view)
            # We'll rely on response.text/content
            try:
                req_body = response.request.content.decode('utf-8', errors='replace') if response.request.content else ""
            except:
                req_body = "[Binary Content]"

            log = TrafficLog(
                id=self.request_counter,
                timestamp=datetime.now().strftime("%H:%M:%S"),
                method=response.request.method,
                url=str(response.request.url),
                status_code=response.status_code,
                request_headers=req_headers,
                request_body=req_body,
                response_headers=res_headers,
                response_body=response.text
            )
            self.log_callback(log)

    async def upload_file(self, 
                          url: str, 
                          file_field_name: str, 
                          filename: str, 
                          file_content: bytes, 
                          content_type: str,
                          extra_data: Optional[Dict] = None,
                          method: str = "POST") -> httpx.Response:
        
        files = {
            file_field_name: (filename, file_content, content_type)
        }
        
        try:
            logger.debug(f"Uploading {filename} to {url}")
            if method.upper() == "POST":
                response = await self.client.post(url, files=files, data=extra_data)
            elif method.upper() == "PUT":
                # PUT usually takes raw body, but here we simulate multipart if needed or raw
                # For file upload vulnerabilities via PUT, it's often raw content
                response = await self.client.put(url, content=file_content)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            self._log_traffic(response)
            return response
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise

    async def check_file_existence(self, url: str) -> httpx.Response:
        """
        Checks if an uploaded file exists/executes by GETting it.
        """
        try:
            response = await self.client.get(url)
            self._log_traffic(response)
            return response
        except Exception as e:
            logger.error(f"Existence check failed: {str(e)}")
            raise

    async def close(self):
        await self.client.aclose()
