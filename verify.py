import sys
import os
import asyncio

# Ensure path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Checking imports...")
    from upload_forge.core.scanner import Scanner
    from upload_forge.core.payloads import PayloadGenerator
    from upload_forge.utils.logger import logger
    from upload_forge.cli.cli_interface import app
    from upload_forge.reporting.html_report import generate_html_report
    print("Imports successful.")

    print("Checking Scanner instantiation...")
    scanner = Scanner()
    print("Scanner instantiated.")
    
    print("Checking Payload generation...")
    gen = PayloadGenerator()
    payloads = gen.generate_all_payloads()
    print(f"Generated {len(payloads)} payloads.")
    
    print("All checks passed.")

except Exception as e:
    print(f"Verification failed: {e}")
    import traceback
    traceback.print_exc()
