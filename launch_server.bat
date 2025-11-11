@echo off
echo ===============================================
echo   SECURE SFTP SERVER - INTERACTIVE LAUNCHER
echo ===============================================
echo Computer Security Group Assignment
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "main.py" (
    echo ERROR: Please run this script from the Computer_Security directory
    echo Current directory: %CD%
    pause
    exit /b 1
)

REM Check dependencies
echo Checking dependencies...
python -c "import asyncssh" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required dependencies...
    pip install asyncssh pytest
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Dependencies OK
echo.

REM Launch interactive server
echo Starting interactive SFTP server launcher...
echo.
python start_server.py

echo.
echo Server stopped. Press any key to exit...
pause >nul