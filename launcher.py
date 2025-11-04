import os
import sys
import subprocess
import socket
import time
import webbrowser
from pathlib import Path

# ================================================
# ⚙️ Auto Django Launcher (Safe & Stable)
# ================================================

BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SMS.settings")

def get_free_port(start_port=8000, max_tries=20):
    """Find a free port to avoid conflicts."""
    port = start_port
    for _ in range(max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError("No available port found!")

def is_server_running(port):
    """Check if something is already running on the port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(("127.0.0.1", port)) == 0

def launch_server():
    """Launch Django server silently in the background."""
    manage_py = BASE_DIR / "manage.py"
    port = get_free_port()
    url = f"http://127.0.0.1:{port}/"

    # Start server silently
    subprocess.Popen(
        [sys.executable, str(manage_py), "runserver", f"127.0.0.1:{port}"],
        cwd=str(BASE_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    )

    # Wait until server responds
    for _ in range(30):
        if is_server_running(port):
            webbrowser.open(url)
            print(f"✅ Server started at {url}")
            return
        time.sleep(1)

    print("❌ Server failed to start.")

if __name__ == "__main__":
    launch_server()

    # Keep the launcher alive just enough
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        pass
