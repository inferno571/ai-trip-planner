@echo off
echo ==========================================
echo    AI Trip Planner - Instant Launcher
echo ==========================================
echo.

:: Save the project directory
set "PROJECT_DIR=%~dp0"

:: Step 1: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)
echo [OK] Python found.

:: Step 2: Create venv if it doesn't exist
if not exist "%PROJECT_DIR%venv\Scripts\activate.bat" (
    echo [INFO] Creating virtual environment...
    python -m venv "%PROJECT_DIR%venv"
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
)

:: Step 3: Install dependencies if uvicorn is missing
if not exist "%PROJECT_DIR%venv\Scripts\uvicorn.exe" (
    echo [INFO] Installing dependencies... This may take a few minutes.
    call "%PROJECT_DIR%venv\Scripts\activate.bat"
    python -m pip install --upgrade pip
    pip install -r "%PROJECT_DIR%requirements.txt"
    pip install -e "%PROJECT_DIR%."
    echo [OK] Dependencies installed.
) else (
    echo [OK] Dependencies already installed.
)

:: Step 4: Verify uvicorn exists
if not exist "%PROJECT_DIR%venv\Scripts\uvicorn.exe" (
    echo [ERROR] uvicorn was not installed. Check requirements.txt or your internet connection.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo    Launching Application...
echo ==========================================
echo.

:: Step 5: Start Backend (FastAPI) in a NEW window
echo [INFO] Starting Backend on http://localhost:8000 ...
start "Backend - FastAPI" cmd /k "cd /d "%PROJECT_DIR%" && call venv\Scripts\activate.bat && python -m uvicorn main:app --reload --port 8000"

:: Wait a moment for the backend to start
timeout /t 3 /nobreak >nul

:: Step 6: Start Frontend (Streamlit) in THIS window
echo [INFO] Starting Frontend on http://localhost:8501 ...
cd /d "%PROJECT_DIR%"
call venv\Scripts\activate.bat
python -m streamlit run streamlit_app.py

pause
