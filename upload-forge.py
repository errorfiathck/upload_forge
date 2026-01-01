import sys
import os

# Ensure the package is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from upload_forge.cli.cli_interface import app

def main():
    app()

if __name__ == "__main__":
    main()
