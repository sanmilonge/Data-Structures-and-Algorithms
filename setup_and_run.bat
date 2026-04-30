@echo off
REM Batch script to install latest Python and required packages for this project

REM Check if Python is installed
set "PYTHON_JUST_INSTALLED=0"
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python not found. Downloading and installing latest Python...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe -OutFile python-latest.exe"
    start /wait python-latest.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    del python-latest.exe
    echo Python installed.
    set "PYTHON_JUST_INSTALLED=1"
) ELSE (
    echo You already have python installed. Skipping installation step.
)

REM Check for pip
python -m ensurepip --upgrade

REM Upgrade pip
python -m pip install --upgrade pip

REM Install curses
pip install windows-curses

echo.
if "%PYTHON_JUST_INSTALLED%"=="1" (
    echo Setup complete, but Python was just installed.
    echo Restart your terminal and ensure python is added to your path then run this script again to play!
    pause
    exit /b 0
) else (
    echo Setup complete. You can now run the program.
    echo.
    echo Which script do you want to run?
    echo   1. main.py (better UI)
    echo   2. main1.py (text based UI)
    set /p choice="Enter 1 or 2 and press Enter: "
    if "%choice%"=="1" (
        python main.py
    ) else if "%choice%"=="2" (
        python main1.py
    ) else (
        echo Invalid choice. Exiting.
        exit /b 1
    )
)
