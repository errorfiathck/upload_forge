import random
import string
import os

def generate_random_string(length: int = 8) -> str:
    """
    Generates a random string of fixed length.
    """
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_filename(extension: str = "txt") -> str:
    """
    Generates a random filename.
    """
    name = generate_random_string(8)
    return f"{name}.{extension}"

def read_file_content(filepath: str) -> bytes:
    """
    Reads file content as bytes.
    """
    if not os.path.exists(filepath):
        return b""
    with open(filepath, "rb") as f:
        return f.read()
