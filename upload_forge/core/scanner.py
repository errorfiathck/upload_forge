import asyncio
from typing import List, Optional
from .payloads import PayloadGenerator
from .request_engine import RequestEngine
from .response_analyzer import ResponseAnalyzer
from .upload_logic import UploadLogic
from .vulnerability_models import ScanResult, VulnerabilityFinding
from ..utils.logger import logger
from datetime import datetime

class Scanner:
    def __init__(self):
        self.payload_gen = PayloadGenerator()
        self.analyzer = ResponseAnalyzer()
        self.results = []
        self.running = False

    async def scan(self, 
                   target_url: str, 
                   file_param: str = "file",
                   upload_dir: Optional[str] = None,
                   proxies: Optional[dict] = None,
                   headers: Optional[dict] = None,
                   on_log_callback: Optional[callable] = None,
                   on_finding_callback: Optional[callable] = None) -> ScanResult:
        
        self.running = True
        start_time = datetime.now()
        engine = RequestEngine(proxies=proxies, headers=headers)
        
        # Better: Pass on_log_callback to logic -> engine
        engine.set_log_callback(on_log_callback)
        
        logic = UploadLogic(engine, self.analyzer)
        
        scan_result = ScanResult(target=target_url, start_time=start_time)
        
        logger.info(f"Starting scan on {target_url}")
        
        payloads = self.payload_gen.generate_all_payloads()
        
        # In a real tool, we'd use a semaphore for concurrency
        # For now, sequential or simple gather
        
        tasks = []
        for payload in payloads:
            if not self.running: break
            
            # Create specific tasks (or run sequentially for better logging control in this prototype)
            # We'll run sequentially to simulate "Live Scan Monitor" updates easier in GUI later without complex callback logic yet
            logger.info(f"Testing payload: {payload['desc']}")
            finding = await logic.test_payload(target_url, file_param, payload, upload_dir)
            
            if finding:
                logger.warning(f"Vulnerability Found: {finding.name}")
                scan_result.findings.append(finding)
                scan_result.stats["vulns_found"] += 1
                if on_finding_callback:
                    on_finding_callback(finding)
            
            scan_result.stats["total_requests"] += 1

        await engine.close()
        scan_result.end_time = datetime.now()
        self.running = False
        logger.info("Scan completed")
        return scan_result

    def stop(self):
        self.running = False
