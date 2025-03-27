import subprocess
import sys
import os
from pathlib import Path

def start_servers():
    root_dir = Path(__file__).parent
    
    # Set up commands based on platform
    backend_cmd = ["cd", f"{root_dir}\\backend", "&&", "uvicorn", "app.main:app", "--reload"]
    shell = True
    
    try:
        print("Starting backend server...")
        subprocess.Popen(backend_cmd, shell=shell)

        print("Backend is available at: http://localhost:8000")
        print("\nClose the server windows to stop the servers")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_servers()
