if [ ! -d "myenv" ]; then
    python -m venv myenv
    powershell -Command "$policy = Get-ExecutionPolicy -Scope Process; if ($policy -ne 'Bypass') { Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force }"
    echo "Installing dependencies..."
    myenv/bin/pip install -r requirements.txt

    read -p "Type in the name of your microphone: " set_mic
    echo "input_mic=\"${set_mic}\"" > src/mic.py
fi

echo "Downloaded necessary dependencies."
echo "Loading..."
myenv/bin/python -m src.Painter
