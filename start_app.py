import os
import sys
import subprocess
import time
import webbrowser
import socket
from pathlib import Path

# =========================================
# ⚙️ SMART DJANGO PROJECT LAUNCHER (LOOP-PROOF)
# =========================================

BASE_DIR = Path(__file__).resolve().parent
VENV_DIR = BASE_DIR / "venv"
PYTHON_EXE = VENV_DIR / "Scripts" / "python.exe"
MANAGE_PY = BASE_DIR / "manage.py"
DEPS_FLAG = BASE_DIR / ".deps_done"

REQUIRED_PACKAGES = [
    "django>=4.2",
    "psutil",
    "pandas",
    "requests",
    "django-jazzmin",
    "xhtml2pdf",
    "channels",
    "channels_redis",
    "pywin32",
    "winshell",
]


def get_local_ip():
    """Get LAN/Wi-Fi IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


HOST = get_local_ip()
PORT = "8000"
URL = f"http://{HOST}:{PORT}/"


# =========================================
# 🧩 Safe Command Runner
# =========================================
def run_command(command, silent=False):
    """Run shell command and print errors if any."""
    try:
        subprocess.run(
            command,
            check=True,
            stdout=None if not silent else subprocess.DEVNULL,
            stderr=None if not silent else subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {command}\n{e}")


# =========================================
# 🧠 Environment Setup
# =========================================
def ensure_venv():
    """Create virtual environment if missing."""
    if not VENV_DIR.exists():
        print("⚙️ Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)


def ensure_dependencies():
    """Install dependencies once, mark completion."""
    if DEPS_FLAG.exists():
        print("✅ Dependencies already installed.")
        return

    print("📦 Installing dependencies...")
    for pkg in REQUIRED_PACKAGES:
        subprocess.run([str(PYTHON_EXE), "-m", "pip", "install", pkg, "-i", "https://pypi.org/simple"], check=True)

    DEPS_FLAG.touch()
    print("✅ All dependencies installed.")


# =========================================
# 🛠️ Database Migration
# =========================================
def apply_migrations():
    """Apply Django migrations safely."""
    print("🔧 Applying migrations...")
    run_command([str(PYTHON_EXE), str(MANAGE_PY), "makemigrations"], silent=False)
    run_command([str(PYTHON_EXE), str(MANAGE_PY), "migrate"], silent=False)


# =========================================
# 🚀 Run Server
# =========================================
def start_server():
    """Start the Django server."""
    print(f"✅ Server ready at {URL}")
    webbrowser.open(URL)
    subprocess.run([str(PYTHON_EXE), str(MANAGE_PY), "runserver", f"{HOST}:{PORT}"], cwd=str(BASE_DIR))


# =========================================
# 🏁 MAIN
# =========================================
def main():
    print("🔄 Preparing environment...")
    ensure_venv()

    # Use the venv Python from now on
    if str(sys.executable) != str(PYTHON_EXE):
        print("🔁 Restarting inside virtual environment...")
        os.execv(str(PYTHON_EXE), [str(PYTHON_EXE), __file__])

    ensure_dependencies()
    apply_migrations()
    start_server()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user. Exiting gracefully...")
        sys.exit(0)
