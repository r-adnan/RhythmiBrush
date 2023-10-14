@echo off
echo Setting up environment...

SETLOCAL ENABLEDELAYEDEXPANSION
if NOT EXIST myenv (
    call python -m venv myenv 
    powershell -Command "$policy = Get-ExecutionPolicy -Scope Process; if ($policy -ne 'Bypass') { Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force }"
    echo Installing dependencies...
    call .\myenv\Scripts\pip install -r requirements.txt > NUL 2>&1

    set /p set_mic=Type in the name of your microphone: 
    echo input_mic = "!set_mic!" > src/mic.py
)

echo Downloaded necessary dependencies.
echo Loading...
call .\myenv\Scripts\python -m src.Painter






