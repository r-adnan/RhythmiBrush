if [ ! -d "myenv" ]; then
    python -m venv myenv
    myenv/bin/pip install -r requirements.txt
fi

echo "Downloaded necessary dependencies..."
echo "Loading..."
myenv/bin/python -m src.Painter
