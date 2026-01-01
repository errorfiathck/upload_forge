import json
from dataclasses import asdict
from ..core.vulnerability_models import ScanResult

def generate_json_report(scan_result: ScanResult, filename: str):
    """
    Exports scan results to a JSON file.
    """
    # Convert dataclass to dict, handling datetime serialization
    def default_serializer(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        return str(obj)

    data = asdict(scan_result)
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, default=default_serializer)
    
    print(f"Report saved to {filename}")
