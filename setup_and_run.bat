@echo off
:: check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed
    pause
    exit /b
)

:: create a virtual environment
echo Creating a virtual environment...
python -m venv creative_core_venv

:: activate the virtual environment
call creative_core_venv\Scripts\activate

:: install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

:: launch the game
echo Launching the game, enjoy !
echo credits : PouchyCorp, Tioh, Ytyt, Leih
python sources\main.py

:: deactivate the environment after exiting the game
call creative_core_venv\Scripts\deactivate
