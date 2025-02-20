@echo off

:: create a virtual environment
echo Creating a virtual environment...
python -m venv server_venv

:: activate the virtual environment
call server_venv\Scripts\activate

:: launch the game
echo credits : PouchyCorp, Tioh, Ytyt, Leih
echo Launching server ...
python database_server.py

:: deactivate the environment after exiting the game
call creative_core_venv\Scripts\deactivate
