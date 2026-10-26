import sys
import time
import subprocess
import urllib.request
import json
import os

sys.path.insert(0, os.path.abspath("."))

def main():
    print("Starting uvicorn server in background...")
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    try:
        time.sleep(2.5)
        # Test 1: Health endpoint
        with urllib.request.urlopen("http://127.0.0.1:8000/api/v1/health") as resp:
            health = json.loads(resp.read().decode())
            print("[SUCCESS] Health Endpoint:", health)

        # Test 2: Careers Knowledge Base
        with urllib.request.urlopen("http://127.0.0.1:8000/api/v1/careers/") as resp:
            careers = json.loads(resp.read().decode())
            print(f"[SUCCESS] Knowledge Base seeded with {len(careers)} roles:")
            for c in careers:
                print(f"  • {c['title']} [{c['category']}]")

        print("\nAll live backend endpoints responding perfectly!")
    finally:
        proc.terminate()
        proc.wait()
        print("Server process shut down cleanly.")

if __name__ == "__main__":
    main()
