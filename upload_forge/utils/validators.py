from urllib.parse import urlparse
import re

def is_valid_url(url: str) -> bool:
    """
    Validates if the provided string is a valid URL.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def validate_method(method: str) -> bool:
    """
    Validates HTTP method.
    """
    return method.upper() in ["GET", "POST", "PUT", "PATCH"]

def sanitize_filename(filename: str) -> str:
    """
    Basic filename sanitization (though we often want to bypass this in the scanner).
    """
    return re.sub(r'[^\w\-_\. ]', '_', filename)
