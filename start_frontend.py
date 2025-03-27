import subprocess
import sys
import os
from pathlib import Path

def start_servers():
    root_dir = Path(__file__).parent
    
    # Set up commands based on platform
    frontend_cmd = ["cd", f"{root_dir}\\frontend", "&&", "npm", "run", "dev"]
    shell = True
    
    try:
        print("Starting frontend server...")
        subprocess.Popen(frontend_cmd, shell=shell)
        
        print("\nServers are starting in separate windows!")
        print("Frontend is available at: http://localhost:5173")
        print("\nClose the server windows to stop the servers")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_servers()
