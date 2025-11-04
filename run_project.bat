@echo off
rem -------------------------
rem run_project.bat
rem Portable runner that finds its folder, uses bundled Python if present,
rem creates a venv if needed, installs deps locally, runs migrations, opens browser.
rem -------------------------

REM Get script directory (works even if run from a shortcut)
set SCRIPT_DIR=%~dp0
REM remove trailing backslash
if "%SCRIPT_DIR:~-1%"=="\" set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

echo Running from: %SCRIPT_DIR%

REM Candidate python paths (relative)
set EMBED_PY=%SCRIPT_DIR%\python-embed\python.exe
set LOCAL_PY=%SCRIPT_DIR%\venv\Scripts\python.exe
set SYSTEM_PY=

REM Try system python if nothing else found
where python >nul 2>nul
if %ERRORLEVEL%==0 set SYSTEM_PY=%~$PATH:python.exe%

REM Choose python executable preferring: local venv -> embedded -> system
if exist "%LOCAL_PY%" (
  set PY_EXE=%LOCAL_PY%
) else if exist "%EMBED_PY%" (
  set PY_EXE=%EMBED_PY%
) else if defined SYSTEM_PY (
  set PY_EXE=%SYSTEM_PY%
) else (
  echo No Python found. Please include python-embed/ or allow the script to create a venv with system Python.
  pause
  exit /b 1
)

echo Using Python: %PY_EXE%

REM If we are using embeddable, it may not have pip. We'll try to use ensurepip or fallback.
"%PY_EXE%" -c "import sys; print(sys.executable)" >nul 2>&1
if %ERRORLEVEL% neq 0 (
  echo Python failed to run. Exiting.
  pause
  exit /b 1
)

REM If no local venv, try to create one using the chosen interpreter (skip if interpreter is embeddable that can't create venv)
if not exist "%SCRIPT_DIR%\venv\Scripts\activate" (
  echo Creating local venv...
  "%PY_EXE%" -m venv "%SCRIPT_DIR%\venv" 2>nul
  if %ERRORLEVEL% neq 0 (
    echo Failed to create venv with %PY_EXE%. If you're using the embeddable distribution, ensure the embeddable supports venv or include a full portable python.
    rem If embeddable created no venv, try to use embeddable directly
  ) else (
    echo Activating venv and installing pip...
    call "%SCRIPT_DIR%\venv\Scripts\activate.bat"
    "%SCRIPT_DIR%\venv\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel
  )
)

rem Activate venv if present
if exist "%SCRIPT_DIR%\venv\Scripts\activate.bat" (
  call "%SCRIPT_DIR%\venv\Scripts\activate.bat"
  set PY_EXE=%SCRIPT_DIR%\venv\Scripts\python.exe
  echo Activated venv python: %PY_EXE%
)

REM Install requirements if requirements.txt exists and not flagged yet
if exist "%SCRIPT_DIR%\requirements.txt" (
  echo Installing requirements from requirements.txt (local only)...
  "%PY_EXE%" -m pip install -r "%SCRIPT_DIR%\requirements.txt" --no-warn-script-location
)

REM Run migrations
echo Applying migrations...
"%PY_EXE%" "%SCRIPT_DIR%\manage.py" makemigrations
"%PY_EXE%" "%SCRIPT_DIR%\manage.py" migrate

REM Open browser and start dev server (bound to local IP)
for /f "usebackq tokens=*" %%i in (`"%PY_EXE% - <<PYCODE
import socket
try:
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8',80))
    ip=s.getsockname()[0]
    s.close()
except Exception:
    ip='127.0.0.1'
print(ip)
PYCODE"`) do set LOCALIP=%%i

if not defined LOCALIP set LOCALIP=127.0.0.1
set PORT=8000
set URL=http://%LOCALIP%:%PORT%/

echo Opening %URL%
start "" "%URL%"

echo Starting Django dev server...
"%PY_EXE%" "%SCRIPT_DIR%\manage.py" runserver %LOCALIP%:%PORT%
pause
