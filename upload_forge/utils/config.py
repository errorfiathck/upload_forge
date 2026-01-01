from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).parent.parent

# Asset Paths
PAYLOADS_DIR = PROJECT_ROOT / "assets" / "payload_samples"

# Default Settings
DEFAULT_TIMEOUT = 10
DEFAULT_USER_AGENT = "UploadForge/1.0 (Security Scanner)"
DEFAULT_CONCURRENCY = 10

# Risk Levels
RISK_LOW = "Low"
RISK_MEDIUM = "Medium"
RISK_HIGH = "High"
RISK_CRITICAL = "Critical"

# Detection Confidence
CONFIDENCE_LOW = "Low"
CONFIDENCE_MEDIUM = "Medium"
CONFIDENCE_HIGH = "High"
CONFIDENCE_CERTAIN = "Certain"
