@echo off
setlocal

REM Development environment bootstrap script (Windows)
set "ROOT_DIR=%~dp0.." 
cd /d "%ROOT_DIR%"

echo [dev-setup] Initializing Python venv and Node deps...

REM Python environment
if not exist "venv" (
  echo Creating Python virtual environment (venv) ...
  python -m venv venv
)
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
if exist "requirements.txt" (
  echo Installing Python dependencies...
  pip install -r requirements.txt
)

REM Node/Frontend dependencies
if exist frontend (
  echo Installing Node.js workspace dependencies...
  cd frontend
  call npm install --workspaces
  cd ..
)

echo [dev-setup] Done. Activate venv with: call venv\Scripts\activate.bat
