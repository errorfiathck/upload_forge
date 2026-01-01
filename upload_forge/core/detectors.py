from abc import ABC, abstractmethod
from typing import List, Optional
from .request_engine import RequestEngine
from .response_analyzer import ResponseAnalyzer
from .vulnerability_models import VulnerabilityFinding
from ..utils.logger import logger
from ..utils.config import *

class BaseDetector(ABC):
    def __init__(self, request_engine: RequestEngine, analyzer: ResponseAnalyzer):
        self.engine = request_engine
        self.analyzer = analyzer

    @abstractmethod
    async def run(self, target_url: str, **kwargs) -> List[VulnerabilityFinding]:
        pass

class UnrestrictedFileUploadDetector(BaseDetector):
    async def run(self, target_url: str, **kwargs) -> List[VulnerabilityFinding]:
        # This is handled by the main scanner loop iterating payloads
        # But we could have specific logic here for "plain upload"
        return []

# We might keep the logic in Scanner for now to avoid over-engineering 
# given the time constraints, but keeping the file for future extensibility.
