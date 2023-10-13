@echo off
echo Setting up environment...
if NOT EXIST myenv (
    call python -m venv myenv 
    powershell -Command "$policy = Get-ExecutionPolicy -Scope Process; if ($policy -ne 'Bypass') { Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force }"
    echo Installing dependencies...
    call .\myenv\Scripts\pip install -r requirements.txt > NUL 2>&1
)
echo Downloaded necessary dependencies...
echo Loading...
call .\myenv\Scripts\python -m src.Painter






