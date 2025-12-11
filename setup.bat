@echo off
title Playwright Automation Framework Setup
echo =============================================================
echo                PLAYWRIGHT PYTHON SETUP SCRIPT
echo =============================================================

REM -------------------------------------------------------------
REM STEP 1: CHECK PYTHON INSTALLATION
REM -------------------------------------------------------------
echo [INFO] Checking Python installation...
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERROR] Python is not installed or not added to PATH.
    echo Install Python 3.10+ and rerun this script.
    pause
    exit /b
)
echo [OK] Python found.

REM -------------------------------------------------------------
REM STEP 2: CLEAN OLD VENV (OPTIONAL)
REM -------------------------------------------------------------
IF EXIST venv (
    echo [INFO] Removing old virtual environment...
    rmdir /S /Q venv
)

REM -------------------------------------------------------------
REM STEP 3: CREATE NEW VIRTUAL ENVIRONMENT
REM -------------------------------------------------------------
echo [INFO] Creating new virtual environment: venv
python -m venv venv

IF NOT EXIST venv (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b
)
echo [OK] Virtual environment created.

REM -------------------------------------------------------------
REM STEP 4: ACTIVATE VIRTUAL ENVIRONMENT
REM -------------------------------------------------------------
echo [INFO] Activating virtual environment...
call venv\Scripts\activate

IF "%VIRTUAL_ENV%"=="" (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b
)
echo [OK] Virtual environment activated.

REM -------------------------------------------------------------
REM STEP 5: INSTALL PYTHON DEPENDENCIES
REM -------------------------------------------------------------
IF NOT EXIST requirements.txt (
    echo [ERROR] requirements.txt not found in project root.
    pause
    exit /b
)

echo [INFO] Installing dependencies from requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt

IF ERRORLEVEL 1 (
    echo [ERROR] Failed to install Python dependencies.
    pause
    exit /b
)
echo [OK] Requirements installed.

REM -------------------------------------------------------------
REM STEP 6: INSTALL PLAYWRIGHT BROWSERS
REM -------------------------------------------------------------
echo [INFO] Installing Playwright browsers...
playwright install

IF ERRORLEVEL 1 (
    echo [ERROR] Playwright browser installation failed.
    pause
    exit /b
)
echo [OK] Playwright browsers installed.

REM -------------------------------------------------------------
REM STEP 7: VALIDATE PLAYWRIGHT VERSION
REM -------------------------------------------------------------
echo [INFO] Checking Playwright version...
playwright --version

echo.
echo =============================================================
echo                 SETUP COMPLETED SUCCESSFULLY
echo You can now run UI tests using:
echo.
echo      pytest
echo.
echo =============================================================
pause
exit /b
