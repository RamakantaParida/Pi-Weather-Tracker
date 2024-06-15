@echo off

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed.
    echo Please install Python before running this script.
    pause
    exit /b
)

REM Check for each library and install if not found
python -m pip show serial || python -m pip install pyserial
python -m pip show customtkinter || python -m pip install customtkinter
python -m pip show Pillow || python -m pip install Pillow
python -m pip show opencv-python || python -m pip install opencv-python
python -m pip show numpy || python -m pip install numpy
python -m pip show pyzbar || python -m pip install pyzbar

REM Run the scann.py script
python scann.py Wifi_Wizard
